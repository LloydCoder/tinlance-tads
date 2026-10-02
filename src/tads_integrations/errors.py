"""Shared integration-boundary errors."""


class IntegrationAdapterError(RuntimeError):
    """External integration failed its safety or contract checks."""
