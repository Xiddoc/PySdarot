from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

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

    def search(self, query: str) -> List[Show]:
        """
        Queries the search bar.

        :param query: The query string to pass.
        :return: A list of Show objects.
        """
        # Get the ENTIRE search page
        resp = self.__s.get("/search", params={'term': query})
        """
        Get the shows by iterating per row.
        This is better since it will not be impacted if Sdarot changes
        the CSS classes they use for show elements.
        """
        bs = BeautifulSoup(resp.text, 'html.parser')
        slist = bs.find(id='seriesList')
        # Get all rows
        rows: List[Tag] = slist.find_all(attrs={'class': 'row'})
        # For each row, extract their shows
        shows: List[Tag] = []
        for row in rows:
            shows.extend(row.find_all('div', recursive=False))

        # Build the show objects
        show_objs: List[Show] = []
        for show in shows:
            # Extract show ID
            show_id = int(show.find('a')['href'].removeprefix('/watch/').split('-', 1)[0])
            # Build show and add it to final list
            show_objs.append(
                Show(
                    show_id=show_id,
                    he_name=show.find('h4').text,
                    en_name=show.find('h5').text
                )
            )

        return show_objs

    def small_search(self, query: str) -> List[Show]:
        """
        Queries the search bar.
        This is based on the autocomplete feature, and hence might run a bit faster.
        This search type will return up to 15 results **MAXIMUM**.

        :param query: The query string to pass.
        :return: A list of Show objects.
        """
        # Perform error checking for endpoint
        resp = self.__s.get("/ajax/index", params={'search': query})
        # Get output as Show objects
        shows = []
        for show in resp.json():
            # Split the name, autocomplete gives us a full string
            he_name, en_name = show['name'].split(' / ')
            # Create the show and add it to the list
            shows.append(
                Show(
                    show_id=show['id'],
                    en_name=en_name,
                    he_name=he_name
                )
            )

        return shows
