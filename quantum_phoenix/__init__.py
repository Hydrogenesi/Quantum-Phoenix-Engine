"""Quantum Phoenix Engine — Two Operators, Two Laws Per Step.

A four-state finite state machine driven by operator pairs and transition laws,
burning down eight beats from MERGE to APEX.
"""

from .engine import Phoenix, State
from .icons import ICONS

__version__ = "1.0.0"
__author__ = "James Stanley"
__all__ = ["Phoenix", "State", "ICONS"]
