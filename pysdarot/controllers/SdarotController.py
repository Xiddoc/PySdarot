from requests import Session, Response


# Shamelessly stolen from: https://stackoverflow.com/a/6798042/11985743
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SdarotController(Session, metaclass=Singleton):
    """
    Maybe in future, using a singleton is better since
    it will use only 1 request for the entire session.
    """

    def __init__(self, sdarot_base: str = None) -> None:
        super().__init__()

        # The first time we are called, we must get the Sdarot base URL
        # If we call this later, the singleton metaclass will catch it.
        # Therefore, if we get 'None' now as the parameter, there is an issue.
        if not sdarot_base:
            raise Exception(
                "No Sdarot URL found, make sure you have made an instance of the PySdarot class at least once. "
                "If you have and are still facing this issue, then please report this as a bug."
            )

        # Singletons don't need static classes, we can write this directly to the property
        self.__sdarot_base = sdarot_base

        # Initialize the session with fake UA
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'origin': self.__sdarot_base,
            'referer': self.__sdarot_base
        })

        # Get initial 'anon'/guest cookies
        self.get(self.__sdarot_base)

        # Add base URL to relative paths
        self.request = self.request_override

    def request_override(self, method: str, relative_url: str, **kwargs) -> Response:
        return super().request(
            method=method,
            url=self.__sdarot_base + relative_url,
            **kwargs
        )
