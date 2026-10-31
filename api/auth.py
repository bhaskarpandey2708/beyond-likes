"""
API Key Authentication, Multi-Tenant Quotas & Tiered Rate Limiting Middleware
Enforces tenant status, monthly quotas, scoped permissions, and sliding-window rate limits.
"""
import time
import json
from typing import Optional, Tuple, Dict, Any, List
from storage.db import get_connection, record_tenant_usage
from config.settings import API_KEYS

DEFAULT_TIERS = {
    "starter": {"rpm": 60, "monthly_limit": 50000},
    "growth": {"rpm": 300, "monthly_limit": 250000},
    "pro": {"rpm": 300, "monthly_limit": 250000},
    "enterprise": {"rpm": 1200, "monthly_limit": 1000000}
}

# In-memory sliding window rate limiter: {key: [timestamp, ...]}
_rate_limits: Dict[str, List[float]] = {}

def verify_api_key(
    api_key: Optional[str],
    required_scope: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Verifies an API key against settings, multi-tenant keys, or legacy SQLite tables.
    Returns (is_valid, error_message, client_data).
    If no key is provided, falls back to open access for local development / dashboard.
    """
    if not api_key:
        return True, None, {
            "tenant_id": "org_default_dev",
            "client_name": "Local Dashboard / Dev",
            "tier": "enterprise",
            "scopes": ["*"],
            "rpm_limit": 1200
        }

    # 1. Configured static partner keys (e.g. from settings)
    if api_key in API_KEYS:
        cfg = API_KEYS[api_key]
        client_name = cfg.get("client", "Internal Partner")
        tier = cfg.get("tier", "enterprise")
        tier_cfg = DEFAULT_TIERS.get(tier, DEFAULT_TIERS["enterprise"])

        now = time.time()
        window = _rate_limits.setdefault(api_key, [])
        _rate_limits[api_key] = [t for t in window if now - t < 60.0]
        if len(_rate_limits[api_key]) >= tier_cfg["rpm"]:
            return False, f"Rate limit exceeded: maximum {tier_cfg['rpm']} requests per minute for {tier} tier.", None
        _rate_limits[api_key].append(now)

        return True, None, {
            "tenant_id": "org_partner_static",
            "client_name": client_name,
            "tier": tier,
            "scopes": ["*"],
            "total_requests": len(_rate_limits[api_key]),
            "rpm_limit": tier_cfg["rpm"]
        }

    # 2. Multi-Tenant API Keys (Enterprise & SaaS workspace tenants)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.key_hash, k.tenant_id, k.key_name, k.scopes_json, k.is_active, k.total_requests,
                   t.name as tenant_name, t.tier, t.monthly_quota, t.status as tenant_status
            FROM tenant_api_keys k
            JOIN tenants t ON k.tenant_id = t.id
            WHERE k.key_hash = ?
        """, (api_key,))
        tenant_row = cursor.fetchone()

        if tenant_row:
            if not tenant_row["is_active"]:
                return False, "This API key has been revoked or deactivated.", None
            if tenant_row["tenant_status"] != "ACTIVE":
                return False, f"Tenant workspace is currently {tenant_row['tenant_status']}.", None

            # Verify Scopes
            scopes = json.loads(tenant_row["scopes_json"] or '["*"]')
            if required_scope and ("*" not in scopes and required_scope not in scopes):
                return False, f"API key lacks required scope '{required_scope}'. Granted: {scopes}", None

            tid = tenant_row["tenant_id"]
            tier = tenant_row["tier"] or "growth"
            tier_cfg = DEFAULT_TIERS.get(tier, DEFAULT_TIERS["growth"])
            monthly_quota = tenant_row["monthly_quota"] or tier_cfg["monthly_limit"]

            # Check Monthly Quota (Rolling 30 days)
            now = time.time()
            start_of_month = now - (30 * 86400)
            cursor.execute("SELECT COUNT(*) as calls FROM tenant_usage_logs WHERE tenant_id = ? AND timestamp >= ?", (tid, start_of_month))
            month_calls = cursor.fetchone()["calls"] or 0
            if month_calls >= monthly_quota:
                return False, f"Monthly quota exceeded ({month_calls}/{monthly_quota}). Please upgrade your tenant tier.", None

            # Sliding Window Rate Limit (60-second window)
            window = _rate_limits.setdefault(api_key, [])
            _rate_limits[api_key] = [t for t in window if now - t < 60.0]
            if len(_rate_limits[api_key]) >= tier_cfg["rpm"]:
                return False, f"Rate limit exceeded: maximum {tier_cfg['rpm']} requests per minute for {tier} tier.", None
            _rate_limits[api_key].append(now)

            # Update key usage statistics
            cursor.execute("""
                UPDATE tenant_api_keys 
                SET total_requests = total_requests + 1, last_used_at = ? 
                WHERE key_hash = ?
            """, (now, api_key))
            conn.commit()

            return True, None, {
                "tenant_id": tid,
                "client_name": tenant_row["tenant_name"],
                "key_name": tenant_row["key_name"],
                "tier": tier,
                "scopes": scopes,
                "monthly_usage": month_calls + 1,
                "monthly_quota": monthly_quota,
                "rpm_limit": tier_cfg["rpm"],
                "total_requests": tenant_row["total_requests"] + 1
            }

        # 3. Fallback to legacy api_keys table
        cursor.execute("SELECT client_name, tier, total_requests FROM api_keys WHERE key_hash = ?", (api_key,))
        legacy_row = cursor.fetchone()
        if not legacy_row:
            return False, "Invalid API key provided.", None

        client_name = legacy_row["client_name"]
        tier = legacy_row["tier"] or "starter"
        tier_cfg = DEFAULT_TIERS.get(tier, DEFAULT_TIERS["starter"])

        now = time.time()
        window = _rate_limits.setdefault(api_key, [])
        _rate_limits[api_key] = [t for t in window if now - t < 60.0]

        if len(_rate_limits[api_key]) >= tier_cfg["rpm"]:
            return False, f"Rate limit exceeded: maximum {tier_cfg['rpm']} requests per minute for {tier} tier.", None

        _rate_limits[api_key].append(now)
        cursor.execute("UPDATE api_keys SET total_requests = total_requests + 1 WHERE key_hash = ?", (api_key,))
        conn.commit()

        return True, None, {
            "tenant_id": "org_legacy",
            "client_name": client_name,
            "tier": tier,
            "scopes": ["*"],
            "total_requests": legacy_row["total_requests"] + 1,
            "rpm_limit": tier_cfg["rpm"]
        }

def record_api_call(client_data: Optional[Dict[str, Any]], endpoint: str):
    """Logs billable call for tenant quota tracking."""
    if not client_data:
        return
    tid = client_data.get("tenant_id")
    if tid and not tid.startswith("org_default_dev"):
        record_tenant_usage(tid, endpoint)
