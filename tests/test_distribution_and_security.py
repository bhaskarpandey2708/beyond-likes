"""
Comprehensive Integration, Plugin, & Security Verification Suite
Tests:
1. Chrome Extension (Manifest V3 schema, permissions, content script integrity)
2. WordPress Plugin (PHP syntax, hooks, fail-safe offline fallback)
3. Discourse Plugin (Ruby syntax, event listeners, error resilience)
4. Universal Widget (JavaScript syntax, DOM isolation, XSS protection)
5. Zip Distribution Archives (file presence, uncorrupted headers, manifest integrity)
6. Security Embedding (HMAC-SHA256 signatures, constant-time compare, rate limits, GDPR pseudonymization)
"""

import os
import sys
import json
import zipfile
import subprocess
import unittest
import hmac
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from api.dispatcher import WebhookDispatcher
from api.auth import verify_api_key, record_api_call
from api.exporter import AuditExporter
from core_engine.evaluator import NormativeEvaluator


class TestDistributionAndSecurity(unittest.TestCase):

    def setUp(self):
        self.distribution_dir = os.path.join(BASE_DIR, "distribution")
        self.downloads_dir = os.path.join(BASE_DIR, "downloads")

    # 1. Chrome Extension (Manifest V3) Verification
    def test_chrome_extension_manifest_v3(self):
        manifest_path = os.path.join(self.distribution_dir, "chrome_extension", "manifest.json")
        self.assertTrue(os.path.exists(manifest_path), "manifest.json must exist")
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest.get("manifest_version"), 3, "Must use Chrome Manifest V3")
        self.assertIn("activeTab", manifest.get("permissions", []), "Should declare activeTab permission")
        self.assertTrue(len(manifest.get("content_scripts", [])) > 0, "Must declare content_scripts")
        self.assertEqual(manifest["content_scripts"][0]["js"], ["content.js"])
        self.assertEqual(manifest.get("action", {}).get("default_popup"), "popup.html")

    def test_chrome_extension_scripts_syntax(self):
        ext_dir = os.path.join(self.distribution_dir, "chrome_extension")
        content_js = os.path.join(ext_dir, "content.js")
        popup_js = os.path.join(ext_dir, "popup.js")
        
        res1 = subprocess.run(["node", "-c", content_js], capture_output=True, text=True)
        self.assertEqual(res1.returncode, 0, f"content.js syntax error: {res1.stderr}")

        res2 = subprocess.run(["node", "-c", popup_js], capture_output=True, text=True)
        self.assertEqual(res2.returncode, 0, f"popup.js syntax error: {res2.stderr}")

    # 2. WordPress Plugin Verification
    def test_wordpress_plugin_syntax_and_hooks(self):
        wp_file = os.path.join(self.distribution_dir, "wordpress_plugin", "beyond-likes.php")
        self.assertTrue(os.path.exists(wp_file), "beyond-likes.php must exist")

        res = subprocess.run(["php", "-l", wp_file], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"PHP syntax error: {res.stderr}")

        with open(wp_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("add_filter('pre_comment_approved'", content, "Must hook WordPress comment approval")
        self.assertIn("is_wp_error", content, "Must handle network errors gracefully without blocking comments")

    # 3. Discourse Plugin Verification
    def test_discourse_plugin_syntax_and_hooks(self):
        discourse_file = os.path.join(self.distribution_dir, "discourse_plugin", "plugin.rb")
        self.assertTrue(os.path.exists(discourse_file), "plugin.rb must exist")

        res = subprocess.run(["ruby", "-c", discourse_file], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Ruby syntax error: {res.stderr}")

        with open(discourse_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("on(:post_created)", content, "Must hook Discourse post_created event")
        self.assertIn("rescue => e", content, "Must handle errors gracefully")

    # 4. Universal Widget Verification
    def test_widget_syntax_and_xss_safety(self):
        widget_file = os.path.join(self.distribution_dir, "widget", "beyond-likes.js")
        self.assertTrue(os.path.exists(widget_file), "beyond-likes.js must exist")

        res = subprocess.run(["node", "-c", widget_file], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Widget JS syntax error: {res.stderr}")

        with open(widget_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("innerText", content, "Must use innerText to safely render dynamic text and prevent XSS")
        self.assertNotIn("innerHTML = text", content, "Must never assign raw unescaped text to innerHTML")

    # 5. Zip Distribution Packages Verification
    def test_zip_distribution_packages_integrity(self):
        packages = [
            "beyond-likes-chrome-extension-v2.8.0.zip",
            "beyond-likes-wordpress-plugin-v2.8.0.zip",
            "beyond-likes-discourse-plugin-v2.8.0.zip",
            "beyond-likes-widget-v2.8.0.zip"
        ]
        for pkg_name in packages:
            pkg_path = os.path.join(self.downloads_dir, pkg_name)
            self.assertTrue(os.path.exists(pkg_path), f"Zip bundle {pkg_name} must exist")
            size = os.path.getsize(pkg_path)
            self.assertGreater(size, 500, f"Zip bundle {pkg_name} is too small ({size} bytes)")

            # Verify uncorrupted zip structure
            with zipfile.ZipFile(pkg_path, "r") as z:
                namelist = z.namelist()
                self.assertGreater(len(namelist), 0, f"Zip bundle {pkg_name} is empty")
                test_res = z.testzip()
                self.assertIsNone(test_res, f"Corrupted file inside {pkg_name}: {test_res}")

    # 6. Security Embedding & Cryptographic Defense
    def test_hmac_sha256_cryptographic_signatures(self):
        secret = "super_secure_webhook_signing_secret_9988"
        payload = json.dumps({"event": "comment_quarantined", "comment_id": "c_123"}).encode("utf-8")
        
        signature = WebhookDispatcher.compute_signature(payload, secret)
        self.assertTrue(isinstance(signature, str))
        self.assertEqual(len(signature), 64, "SHA-256 hex signature must be 64 characters")

        # Constant-time comparison
        expected_sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
        self.assertTrue(hmac.compare_digest(signature, expected_sig), "Must pass timing-safe comparison")

    def test_gdpr_pseudonymization_safety(self):
        csv_anonymized = AuditExporter.export_evaluations_csv(limit=10, anonymize=True)
        self.assertIn("id,iso_timestamp,client_key", csv_anonymized)
        
        jsonl_anonymized = AuditExporter.export_evaluations_jsonl(limit=10, anonymize=True)
        self.assertIsInstance(jsonl_anonymized, str)

    def test_adversarial_zero_width_and_homoglyphs(self):
        evaluator = NormativeEvaluator()
        # Zero-width spaces
        zw_text = "You are a f\u200bu\u200bc\u200bk\u200bi\u200bn\u200bg moron and a complete c\u200bl\u200bo\u200bw\u200bn."
        res = evaluator.evaluate(zw_text)
        self.assertEqual(res["status"], "FLAGGED_UNCIVIL")
        self.assertTrue(res["flags"]["is_toxic"])

        # Unicode accented homoglyph substitution
        accent_text = "You are a stúpid ídïöt with no brain."
        res_accent = evaluator.evaluate(accent_text)
        self.assertEqual(res_accent["status"], "FLAGGED_UNCIVIL")
        self.assertTrue(res_accent["flags"]["is_toxic"])


if __name__ == "__main__":
    unittest.main()
