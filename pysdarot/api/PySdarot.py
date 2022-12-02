from typing import List

from pysdarot.controllers.SdarotController import SdarotController
from pysdarot.api.Show import Show


class PySdarot:
    def __init__(self, sdarot_tld: str) -> None:
        """
        :param sdarot_tld: Sdarot gets banned often, update the TLD (end of the domain, like '.com') via this parameter.
        """
        # TODO test with .tv, cloudflare return 522 error status for timeout
        self.base = "https://sdarot" + sdarot_tld

        # Override the controller's TLD
        SdarotController.sdarot_base = self.base
        # Initialize our session
        self.__s = SdarotController()

    def search(self, query: str) -> List[Show]:
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
