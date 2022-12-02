from time import sleep

from bs4 import BeautifulSoup

from pysdarot.controllers.SdarotController import SdarotController


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

    def download_episode(self, season: int, episode: int) -> bytes:
        """
        Download an episode.
        As of now, this returns the entire video data as a bytes object.
        TODO add filename parameter and buffering.

        :param season: The season to select.
        :param episode: The episode from that season to download.
        :return: The byte data of the episode as a video stream.
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

        return resp


    def urlEncode(self, query):
        return urllib.parse.quote(query)

    def getURL(self):
        data = self.getData()
        maxQ = 0
        try:
            for quality in data["watch"]:
                if int(quality) > maxQ:
                    maxQ = int(quality)
        except KeyError:
            return False
        return "https://{serverName}/w/episode/{quality}/{vidID}.mp4?token={token}&time={time}".format(
            serverName=data["url"], quality=maxQ, vidID=data["VID"], token=data["watch"][str(maxQ)],
            time=str(data["time"]))

    def download_file(self, fileName):
        tempURL = self.getURL()
        if tempURL:
            try:
                with self.__s.get(tempURL, stream=True) as r:
                    with open(fileName, 'wb') as f:
                        try:
                            shutil.copyfileobj(r.raw, f)
                        except:
                            f.close()
                            os.remove(fileName)
                            return False
                        f.close()
                    r.close()
            except requests.exceptions.SSLError:
                return False
        else:
            return tempURL

    def __repr__(self) -> str:
        return f"<Show: {self.name}>"
