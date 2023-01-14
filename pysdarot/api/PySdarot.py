from typing import List

from pysdarot.controllers.SdarotController import SdarotController
from pysdarot.api.Show import Show


class PySdarot:
    def __init__(self, sdarot_tld: str, username: str = None, password: str = None) -> None:
        """
        :param sdarot_tld: Sdarot is banned often, update the TLD (end of the domain, like '.com') via this parameter.
        """
        # TODO test with .tv, cloudflare return 522 error status for timeout
        self.base = "https://sdarot" + sdarot_tld

        # Initialize our session
        self.__s = SdarotController(self.base)

        # Only log in if the user has given both a username and password
        if username and password:
            resp = self.__s.post(
                url='/login',
                data={
                    'location': '/',
                    'username': username,
                    'password': password,
                    'login_remember': '1',
                    'submit_login': '',
                },
                allow_redirects=False
            )

            # The login flow redirects you on success
            if resp.status_code != 301:
                raise ValueError(f"Invalid credentials (username or password).")

    def small_search(self, query: str) -> List[Show]:
        """
        Queries the search bar.

        :param query: The query string to pass.
        :return: A list of Show objects.
        """
        # Perform error checking for endpoint
        resp = self.__s.get(f"/ajax/index?search={query}")
        # Get output as class
        return [
            Show(show_id=show['id'], name=show['name'])
            for show in resp.json()
        ]
