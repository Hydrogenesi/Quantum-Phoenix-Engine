"""Visual icons and representations for each Phoenix state."""

from .engine import State

# Eight-beat output
ICONS = {
    State.MERGE: "●  merge",
    State.REPLICATE: "●● replicate",
    State.DIVIDE: "✖  divide",
    State.ABSOLUTE_ZERO: "❄  absolute_zero",
    State.APEX: "★  apex",
}

# Alternative representations
ALT_ICONS = {
    State.MERGE: "[MERGE]",
    State.REPLICATE: "[REPLICATE]",
    State.DIVIDE: "[DIVIDE]",
    State.ABSOLUTE_ZERO: "[ABSOLUTE_ZERO]",
    State.APEX: "[APEX]",
}
