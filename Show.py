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
        resp = self.__s.get(f"https://www.sdarot.tw/watch/{self.show_id}")

        # In the past, I used to parse this using RegEx, but it's better to use
        # an actual HTML parser since Sdarot changes their HTML sometimes
        bs = BeautifulSoup(resp.text, 'html.parser')

        # Get the "season" unordered list tag
        ul = bs.find(id="season")

        # Get the amount of seasons here
        return len(ul.find_all("li"))

    def get_episode_count(self, season: int):
        pass
        # self.__s.get(
        #     "https://sdarot{ext}/ajax/watch?episodeList={showID}&season={season}".format(ext=self.ext, showID=str(
        #         self.sidraData["SID"]), season=str(self.season))).text, 'data-episode="', '"'))

    def download_show(self, show_id: id, season: int, episode: int) -> bytes:
        # We need to get the show metadata first so we can build the download URL
        sidra_data = self.search(show)

        query_url = f"{self.base}/watch/" \
                    f"{sidra_data['SID']}-{self.urlEncode(sidra_data['Sname'][0])}-{sidra_data['Sname'][1]}/" \
                    f"season/{season}/episode/{episode}"

        self.__s.get(query_url)

    def __repr__(self) -> str:
        return self.name
