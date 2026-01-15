"""Simple switch-case implementation for error handling."""
from typing import Any, Dict, Optional


class SwitchCase:
    """
    Switch-case pattern implementation.

    Usage:
        switch = SwitchCase({"error.Type": "handler"}, "error.Type")
        result = switch.match()  # Returns "handler"
    """

    def __init__(self, case_dictionary: Dict[str, Any], value: str) -> None:
        self.case_dictionary = case_dictionary
        self.value = value

    def match(self, partial: bool = True) -> Optional[str]:
        """
        Find matching case for the value.

        Args:
            partial: If True, checks if case is contained in value.
                    If False, checks for exact match.

        Returns:
            The matched handler/value or "UnknownError" if no match.
        """
        for case, handler in self.case_dictionary.items():
            if partial:
                if case in self.value:
                    return handler
            else:
                if case == self.value:
                    return handler
        return "UnknownError"


# Backwards compatibility alias
switchcase = SwitchCase
