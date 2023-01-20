from shutil import copyfileobj
from time import sleep
from typing import Dict, Optional

from bs4 import BeautifulSoup

from pysdarot.controllers.SdarotController import SdarotController
from pysdarot.handling.errors import SdarotException


class Show:

    def __init__(self, show_id: int, en_name: Optional[str] = None, he_name: Optional[str] = None) -> None:
        self.show_id = show_id
        self.en_name = en_name
        self.he_name = he_name
        self.name = f'{self.he_name} / {self.en_name}'
        self.__s = SdarotController()
        self.__page = None

    def __get_show_html(self) -> str:
        # Download page, set it for cache
        if not self.__page:
            self.__page = self.__s.get(f"/watch/{self.show_id}").text

        return self.__page

    def populate_show_data(self) -> None:
        """
        Populates this object with data about the show,
        including the name of the show in Hebrew and English.
        """
        # Extract the name tag with HTML parsing
        bs = BeautifulSoup(self.__get_show_html(), 'html.parser')
        # NAME TAG LOOKS LIKE THIS:
        # <h1><strong>בית הקנייר / <span class="ltr">Monkey Heist</span></strong></h1>
        name_tag = bs.find(id="watchEpisode").find("h1")

        # Extract the english show name
        en_tag = name_tag.find('span')
        self.en_name = en_tag.text

        # Kill english tag
        en_tag.decompose()
        # Now we can cleanly extract Hebrew name with guarantee of no issues
        self.he_name = name_tag.text.removesuffix(' / ')

    def get_season_count(self) -> int:
        """
        No API endpoint for this, so we need to parse the HTML manually.

        :return: The amount of seasons this show has.
        """
        # In the past, I used to parse this using RegEx, but it's better to use
        # an actual HTML parser since Sdarot changes their HTML sometimes
        bs = BeautifulSoup(self.__get_show_html(), 'html.parser')

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

    def download_episode(self, season: int, episode: int, file_path: str) -> None:
        """
        Download an episode.
        As of now, this returns the entire video data as a bytes object.

        :param season: The season to select.
        :param episode: The episode from that season to download.
        :param file_path: The file to write the episode data to (as a MP4 file format).
        """
        resp = self.__s.post(
            url="/ajax/watch",
            data={
                "preWatch": True,
                "SID": self.show_id,
                "season": season,
                "ep": episode
            }
        )

        # Token is returned in plaintext
        token = resp.text

        # No way to bypass the wait time
        sleep(30)

        # Get the video server
        resp = self.__s.post(
            url="/ajax/watch",
            data={
                "watch": "false",
                "token": token,
                "serie": self.show_id,
                "season": season,
                "episode": episode,
                "type": "episode"
            }
        )

        # Convert to a dictionary
        episode_data: Dict = resp.json()

        # Check if the server threw an error
        if 'watch' not in episode_data:
            raise SdarotException(f"Video not available, maybe the server has too much stress: {episode_data}")

        # Extract the best format available
        # Turns the keys of the video formats into integers, then extracts the maximum integer
        best_format: int = max(map(int, episode_data['watch']))

        # Use the best format for now
        # TODO offer user to choose a format
        vid_url: str = episode_data['watch'][str(best_format)]
        proper_vid_url = "https:" + vid_url

        # Download the episode, open a stream to the download URL and a buffer to the file
        with self.__s.request("GET", proper_vid_url, full_url=True, stream=True) as r, open(file_path, 'wb') as f:
            # This method uses buffering as opposed to downloading the entire request without streaming
            copyfileobj(r.raw, f)

    def __repr__(self) -> str:
        return f"<Show: {self.name}>"
