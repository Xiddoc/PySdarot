from bs4 import BeautifulSoup

from SdarotController import SdarotController


class Show:

    def __init__(self, show_id: int, name: str) -> None:
        self.show_id = show_id
        self.name = name
        self.__s = SdarotController()

    def get_season_count(self) -> int:
        """
        No API endpoint for this, so we need to parse the HTML manually.

        :return: The amount of seasons this show has.
        """
        # Perform error checking later
        resp = self.__s.get(f"/watch/{self.show_id}")

        # In the past, I used to parse this using RegEx, but it's better to use
        # an actual HTML parser since Sdarot changes their HTML sometimes
        bs = BeautifulSoup(resp.text, 'html.parser')

        # Get the "season" unordered list tag
        ul = bs.find(id="season")

        # Get the amount of seasons here
        return len(ul.find_all("li"))

    def get_episode_count(self, season: int) -> int:
        """
        Gets the amount of episodes in a show's specific season.

        :param season: The season to query.
        :return: The amount of epsidoes in this season.
        """
        # TODO Error checking later...
        resp = self.__s.get(
            url="/ajax/watch",
            params={
                "episodeList": self.show_id,
                "season": season
            }
        )

        # In the past, I used to parse this using RegEx, but it's better to use
        # an actual HTML parser since Sdarot changes their HTML sometimes
        bs = BeautifulSoup(resp.text, 'html.parser')

        # Get the list of episodes
        return len(bs.find_all("li", recursive=False))

    def download_show(self, show_id: id, season: int, episode: int) -> bytes:
        # We need to get the show metadata first so we can build the download URL
        sidra_data = self.search(show)

        query_url = f"{self.base}/watch/" \
                    f"{sidra_data['SID']}-{self.urlEncode(sidra_data['Sname'][0])}-{sidra_data['Sname'][1]}/" \
                    f"season/{season}/episode/{episode}"

        self.__s.get(query_url)

    def __repr__(self) -> str:
        return self.name
