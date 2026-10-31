"""
Configuration & Settings for Beyond Likes Discourse Intelligence Engine
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Server Settings
HOST = os.environ.get("BEYOND_LIKES_HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", os.environ.get("BEYOND_LIKES_PORT", 8888)))

# API Authentication (Development default)
API_KEYS = {
    "dev-test-key-001": {"client": "Internal Dev", "tier": "enterprise", "rate_limit_rpm": 600},
    "trial-publisher-key": {"client": "Trial Publisher", "tier": "starter", "rate_limit_rpm": 60}
}

# Dimension Weights for Composite Score (0.0 - 1.0)
DIMENSION_WEIGHTS = {
    "constructiveness": 0.35,
    "civility": 0.25,
    "persuasiveness": 0.20,
    "relevance": 0.20
}

# Quality Gating Thresholds (0 - 100)
THRESHOLDS = {
    "auto_approve": 75,
    "needs_review": 45,
    "auto_reject": 25
}

# Supported Perspective API Attributes for Compatibility
SUPPORTED_PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "IDENTITY_ATTACK",
    "THREAT"
]
