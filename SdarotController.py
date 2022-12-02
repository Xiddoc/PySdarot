from requests import Session, Response


class SdarotController(Session):
    """
    Maybe in future, using a singleton is better since
    it will use only 1 request for the entire session.
    """
    sdarot_base: str = None

    def __init__(self) -> None:
        super().__init__()
        # Initialize the session with fake UA
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'origin': self.sdarot_base,
            'referer': self.sdarot_base
        })

        # Get initial 'anon'/guest cookies
        self.get(self.sdarot_base)

        # Add base URL to relative paths
        self.request = self.request_override

    def request_override(self, method: str, relative_url: str, **kwargs) -> Response:
        return super().request(
            method=method,
            url=self.sdarot_base + relative_url,
            **kwargs
        )
