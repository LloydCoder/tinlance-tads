"""Deterministic signal detection for TADS M4."""

from .detector import SignalDetector
from .models import DetectedSignal, SignalKind

__all__ = ["DetectedSignal", "SignalDetector", "SignalKind"]
