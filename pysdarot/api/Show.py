from shutil import copyfileobj
from time import sleep
from typing import Dict

from bs4 import BeautifulSoup

from pysdarot.controllers.SdarotController import SdarotController
from pysdarot.handling.errors import SdarotException


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
        # TODO perform error checking later
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

    def download_episode(self, season: int, episode: int, file_path: str) -> None:
        """
        Download an episode.
        As of now, this returns the entire video data as a bytes object.

        :param season: The season to select.
        :param episode: The episode from that season to download.
        :param file_path: The file to write the episode data to (as a MP4 file format).
        """
        # TODO error checking...
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
        # TODO error checking
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

        # Download the episode
        # (Python 3.10 supports parenthesis for with statements, but
        # we won't use them so we can adapt to multiple versions of Python)
        with \
                self.__s.request("GET", proper_vid_url, full_url=True, stream=True) as r, \
                open(file_path, 'wb') as f:
            # This method uses buffering as opposed to downloading the entire request without streaming
            copyfileobj(r.raw, f)

    def __repr__(self) -> str:
        return f"<Show: {self.name}>"
