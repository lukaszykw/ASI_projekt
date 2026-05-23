class ExternalApiError(Exception):
    def __init__(
        self,
        source: str,
        message: str,
        status_code: int = 502,
        upstream_status_code: int | None = None,
    ) -> None:
        self.source = source
        self.message = message
        self.status_code = status_code
        self.upstream_status_code = upstream_status_code
        super().__init__(message)
