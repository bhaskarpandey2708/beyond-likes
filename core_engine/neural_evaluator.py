"""
Local Neural Discourse Evaluator (PyTorch CPU Inference Engine)
Loads trained DeBERTa-v3 multi-head regression weights for sub-50ms continuous scoring.
Provides pure neural scoring and enterprise hybrid ensembling.
"""
import os
import sys
import time
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS_PATH = os.path.join(BASE_DIR, "models", "beyond_likes_deberta_weights.pt")

_MODEL_INSTANCE = None
_TOKENIZER_INSTANCE = None
_TORCH_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    from transformers import AutoTokenizer, AutoModel, AutoConfig
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

if _TORCH_AVAILABLE:
    class DeBERTaDiscourseModel(nn.Module):
        def __init__(self, base_model_name: str = "microsoft/deberta-v3-small"):
            super().__init__()
            model_dir = os.path.join(BASE_DIR, "models")
            if os.path.exists(os.path.join(model_dir, "config.json")) and base_model_name == "microsoft/deberta-v3-small":
                self.config = AutoConfig.from_pretrained(model_dir, local_files_only=True)
            else:
                self.config = AutoConfig.from_pretrained(base_model_name)
            self.backbone = AutoModel.from_config(self.config)
            self.dropout = nn.Dropout(0.2)
            self.regressor = nn.Linear(self.config.hidden_size, 4)
            self.sigmoid = nn.Sigmoid()

        def forward(self, input_ids, attention_mask):
            outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
            if hasattr(outputs, "last_hidden_state"):
                pooled = outputs.last_hidden_state[:, 0, :]
            else:
                pooled = outputs[0][:, 0, :]
            logits = self.regressor(self.dropout(pooled))
            return self.sigmoid(logits)

def load_weights_into_model(model, sd):
    first_key = next(iter(sd.keys()))
    if first_key.startswith("encoder.") or first_key.startswith("head."):
        new_sd = {}
        for k, v in sd.items():
            if k.startswith("encoder."):
                new_sd["backbone." + k[len("encoder."):]] = v
            elif k.startswith("head."):
                new_sd["regressor." + k[len("head."):]] = v
            else:
                new_sd[k] = v
        model.load_state_dict(new_sd)
    else:
        model.load_state_dict(sd)

def get_neural_engine():
    """
    Singleton loader for neural model and tokenizer.
    Prioritizes high-capacity scale tiers (435M DeBERTa-large, 395M ModernBERT)
    before falling back to the 44M base model.
    """
    global _MODEL_INSTANCE, _TOKENIZER_INSTANCE
    if not _TORCH_AVAILABLE:
        return None, None

    if _MODEL_INSTANCE is None:
        # Check for large scale models in local or Google Drive mirror
        candidate_dirs = [
            os.path.join(BASE_DIR, "models", "beyond_likes_deberta-v3-large"),
            "/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE/models/beyond_likes_deberta-v3-large",
            os.path.join(BASE_DIR, "models", "beyond_likes_modernbert-large"),
            "/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE/models/beyond_likes_modernbert-large",
        ]

        loaded_large = False
        for cdir in candidate_dirs:
            bin_path = os.path.join(cdir, "pytorch_model.bin")
            q_path = os.path.join(cdir, "quantized_model_qint8.pt")
            cfg_path = os.path.join(cdir, "discourse_config.json")
            if (os.path.exists(bin_path) or os.path.exists(q_path)) and os.path.exists(cfg_path):
                try:
                    import json
                    with open(cfg_path, "r") as f:
                        meta = json.load(f)
                    base_hf = meta.get("base_model", "microsoft/deberta-v3-large")
                    print(f"[*] Loading High-Capacity Neural Model: {meta.get('parameter_count')} ({base_hf})...")
                    model = DeBERTaDiscourseModel(base_model_name=base_hf)
                    weights_file = q_path if os.path.exists(q_path) else bin_path
                    if weights_file == q_path:
                        model = torch.ao.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)
                    sd = torch.load(weights_file, map_location="cpu")
                    load_weights_into_model(model, sd)
                    model.eval()
                    if weights_file != q_path:
                        try:
                            model = torch.ao.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)
                        except Exception:
                            pass
                    _MODEL_INSTANCE = model
                    if os.path.exists(os.path.join(cdir, "tokenizer.json")):
                        _TOKENIZER_INSTANCE = AutoTokenizer.from_pretrained(cdir, local_files_only=True)
                    else:
                        _TOKENIZER_INSTANCE = AutoTokenizer.from_pretrained(base_hf)
                    loaded_large = True
                    break
                except Exception as err:
                    print(f"[!] Warning: Failed loading high-capacity model from {cdir}: {err}")

        # Fallback to trained DeBERTa-v3 44M weights
        if not loaded_large and os.path.exists(WEIGHTS_PATH):
            model = DeBERTaDiscourseModel("microsoft/deberta-v3-small")
            sd = torch.load(WEIGHTS_PATH, map_location="cpu")
            load_weights_into_model(model, sd)
            model.eval()
            try:
                # Dynamic INT8 Quantization for 3x faster CPU execution
                model = torch.ao.quantization.quantize_dynamic(
                    model, {nn.Linear}, dtype=torch.qint8
                )
            except Exception:
                pass
            _MODEL_INSTANCE = model
            model_dir = os.path.join(BASE_DIR, "models")
            if os.path.exists(os.path.join(model_dir, "tokenizer.json")):
                _TOKENIZER_INSTANCE = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
            else:
                _TOKENIZER_INSTANCE = AutoTokenizer.from_pretrained("microsoft/deberta-v3-small")

    return _MODEL_INSTANCE, _TOKENIZER_INSTANCE

class NeuralEvaluator:
    """
    High-capacity neural discourse evaluator utilizing the fine-tuned
    44M-parameter DeBERTa-v3 model.
    """

    def __init__(self):
        self.is_ready = _TORCH_AVAILABLE and os.path.exists(WEIGHTS_PATH)
        self.model = None
        self.tokenizer = None
        if self.is_ready:
            self.model, self.tokenizer = get_neural_engine()

    def evaluate(self, text: str) -> Dict[str, Any]:
        """Runs neural forward pass on input text."""
        if not self.is_ready or not self.model:
            return {"error": "PyTorch/DeBERTa model not initialized or unavailable in this environment"}

        start_time = time.perf_counter()
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )
        
        with torch.no_grad():
            preds = self.model(inputs["input_ids"], inputs["attention_mask"])[0]

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        
        # Dimensions in order: constructiveness, civility, persuasiveness, relevance
        scores = {
            "constructiveness": round(preds[0].item() * 100.0, 1),
            "civility": round(preds[1].item() * 100.0, 1),
            "persuasiveness": round(preds[2].item() * 100.0, 1),
            "relevance": round(preds[3].item() * 100.0, 1)
        }
        
        composite = round(
            (scores["constructiveness"] * 0.35) +
            (scores["civility"] * 0.30) +
            (scores["persuasiveness"] * 0.20) +
            (scores["relevance"] * 0.15),
            1
        )
        
        if scores["civility"] < 35.0:
            status = "FLAGGED_UNCIVIL"
            summary = "Neural model detected hostile attack or harassment."
        elif composite >= 75.0 and scores["civility"] >= 70.0:
            status = "APPROVED_PROMOTED"
            summary = "High-quality epistemic submission verified by neural transformer."
        elif composite >= 50.0:
            status = "STANDARD_PUBLISH"
            summary = "Acceptable community contribution."
        else:
            status = "NEEDS_IMPROVEMENT"
            summary = "Low substance or unsubstantiated argument."

        return {
            "composite_score": composite,
            "status": status,
            "summary": summary,
            "backend": "neural_deberta_v3",
            "dimensions": scores,
            "latency_ms": latency_ms
        }

    def evaluate_hybrid(self, text: str, heuristic_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enterprise Hybrid Ensemble:
        Blends neural semantic depth (70%) with deterministic heuristic rules (30%).
        Applies hard safety floor: if deterministic regex flags toxic or spam, it overrides.
        """
        neural_res = self.evaluate(text)
        if "error" in neural_res:
            # Fall back cleanly to heuristic result
            heuristic_result["backend"] = "heuristic_fallback"
            return heuristic_result

        h_dims = heuristic_result["dimensions"]
        n_dims = neural_res["dimensions"]

        # Weighted blend (70% neural semantic embeddings, 30% heuristic syntactic markers)
        blended_dims = {
            "constructiveness": round(n_dims["constructiveness"] * 0.70 + h_dims["constructiveness"] * 0.30, 1),
            "civility": round(n_dims["civility"] * 0.70 + h_dims["civility"] * 0.30, 1),
            "persuasiveness": round(n_dims["persuasiveness"] * 0.70 + h_dims["persuasiveness"] * 0.30, 1),
            "relevance": round(n_dims["relevance"] * 0.70 + h_dims["relevance"] * 0.30, 1)
        }

        # Hard guardrail overrides
        if heuristic_result.get("flags", {}).get("is_spam", False):
            blended_dims["relevance"] = min(blended_dims["relevance"], 10.0)
            status = "FLAGGED_SPAM"
            summary = "Commercial spam or promotional link intercepted."
        elif heuristic_result.get("flags", {}).get("is_toxic", False) or blended_dims["civility"] < 40.0:
            blended_dims["civility"] = min(blended_dims["civility"], 25.0)
            status = "FLAGGED_UNCIVIL"
            summary = "Hostile personal attack or abusive profanity intercepted."
        else:
            status = neural_res["status"]
            summary = neural_res["summary"]

        weights = {"constructiveness": 0.35, "civility": 0.30, "persuasiveness": 0.20, "relevance": 0.15}
        composite = round(sum(blended_dims[k] * weights[k] for k in weights), 1)

        merged = dict(heuristic_result)
        merged["composite_score"] = composite
        merged["status"] = status
        merged["summary"] = summary
        merged["backend"] = "hybrid_ensemble"
        merged["dimensions"] = blended_dims
        merged["metrics"]["latency_ms"] = round(heuristic_result["metrics"]["latency_ms"] + neural_res["latency_ms"], 2)
        merged["neural_detail"] = {
            "raw_neural_scores": n_dims,
            "neural_latency_ms": neural_res["latency_ms"]
        }
        try:
            from .action_rules import evaluate_action_rules
            merged["action_routing"] = evaluate_action_rules(merged)
        except Exception:
            pass
        return merged
