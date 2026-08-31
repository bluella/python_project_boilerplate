"""Project-specific exception hierarchy.

All domain errors derive from :class:`ProjectError` so callers can catch the whole family
without resorting to bare ``except`` clauses.
"""


class ProjectError(Exception):
    """Base exception for all project errors."""


class DataValidationError(ProjectError):
    """Raised when external data fails schema validation at a boundary."""


class SourceConnectionError(ProjectError):
    """Raised when a data source is unreachable, rejects auth, or errors a request."""
