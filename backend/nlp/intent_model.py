"""
IntentClassifier: MiniLM encoder + trainable Linear classification head.

Architecture:
  Input text
      │
  MiniLM (all-MiniLM-L6-v2) — frozen or partially unfrozen
      │  [CLS] token embedding → 384-dim
      │
  Dropout(0.1)
      │
  Linear(384 → 128)  ← trainable
      │
  ReLU
      │
  Dropout(0.1)
      │
  Linear(128 → 7)    ← trainable (7 intent classes)
      │
  Softmax (at inference) / CrossEntropyLoss (at training)
"""

import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer


class IntentClassifier(nn.Module):
    def __init__(self, num_classes: int = 7, hidden_dim: int = 128, dropout: float = 0.1):
        super().__init__()
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        embed_dim = 384  # MiniLM output dimension

        self.classifier = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(embed_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, num_classes),
        )

    def encode_text(self, texts: list, device: torch.device) -> torch.Tensor:
        """Get [CLS] mean-pooled embeddings from MiniLM as a tensor."""
        embeddings = self.encoder.encode(texts, convert_to_tensor=True, device=device)
        return embeddings  # shape: (batch, 384)

    def forward(self, embeddings: torch.Tensor) -> torch.Tensor:
        """Forward pass through classification head."""
        return self.classifier(embeddings)  # shape: (batch, num_classes)

    def predict(self, text: str, device: torch.device = None) -> tuple:
        """Inference: returns (label_id, confidence)."""
        if device is None:
            device = torch.device("cpu")
        self.eval()
        with torch.no_grad():
            emb = self.encode_text([text], device)
            logits = self.forward(emb)
            probs = torch.softmax(logits, dim=-1)
            label_id = torch.argmax(probs, dim=-1).item()
            confidence = probs[0][label_id].item()
        return label_id, confidence
