"""
Compliance Audit Data Exporter for Beyond Likes
Streams out moderation decisions, appeals, and shadow discrepancy logs in CSV and JSONL formats.
Includes optional GDPR-compliant pseudonymization / redaction.
"""

import csv
import io
import json
import time
from typing import Optional, List, Dict, Any
from storage.db import export_audit_records, get_appeals, get_recent_shadow_logs


class AuditExporter:
    """
    Exports moderation audit logs and regulatory data.
    """

    @staticmethod
    def export_evaluations_csv(limit: int = 1000, anonymize: bool = False) -> str:
        """Exports evaluation audit logs as CSV string."""
        records = export_audit_records(limit=limit, anonymize=anonymize)
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "id",
            "iso_timestamp",
            "client_key",
            "text_hash",
            "text_snippet",
            "word_count",
            "composite_score",
            "status",
            "latency_ms"
        ])

        for r in records:
            iso_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(r["timestamp"]))
            writer.writerow([
                r["id"],
                iso_time,
                r["client_key"],
                r["text_hash"],
                r["text_snippet"],
                r["word_count"],
                r["composite_score"],
                r["status"],
                r["latency_ms"]
            ])

        return output.getvalue()

    @staticmethod
    def export_evaluations_jsonl(limit: int = 1000, anonymize: bool = False) -> str:
        """Exports evaluation audit logs as newline-delimited JSON string."""
        records = export_audit_records(limit=limit, anonymize=anonymize)
        lines = [json.dumps(r) for r in records]
        return "\n".join(lines)

    @staticmethod
    def export_appeals_csv(limit: int = 500) -> str:
        """Exports Article 20 appeals as CSV string."""
        appeals = get_appeals(limit=limit)
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "appeal_id",
            "created_at",
            "user_id",
            "original_status",
            "original_score",
            "appeal_reason",
            "revised_text",
            "revised_score",
            "decision",
            "moderator_notes"
        ])

        for a in appeals:
            iso_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(a["created_at"]))
            writer.writerow([
                a["id"],
                iso_time,
                a["user_id"],
                a["original_status"],
                a["original_score"],
                a["appeal_reason"],
                a.get("revised_text") or "",
                a.get("revised_score") or "",
                a["decision"],
                a.get("moderator_notes") or ""
            ])

        return output.getvalue()
