from typing import Dict, List

import requests
import urllib
import time
import json
import shutil
import os


class Sdarot:
    def __init__(self, sdarot_tld: str) -> None:
        """
        :param sdarot_tld: Sdarot gets banned often, update the TLD (end of the domain, like '.com') via this parameter.
        """
        # TODO test with .tv, cloudflare return 522 error status for timeout
        self.base = "https://sdarot" + sdarot_tld

        # Initialize a session with fake UA
        self.__s = requests.Session()
        self.__s.headers.update({
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'origin': self.base
        })

        # Get initial 'anon' cookies
        self.__s.get(self.base)

    def download_show(self, show: str, season: int, episode: int):
        # We need to get the show metadata first so we can build the download URL
        sidra_data = self.search(show)

        query_url = f"{self.base}/watch/" \
                    f"{sidra_data['SID']}-{self.urlEncode(sidra_data['Sname'][0])}-{sidra_data['Sname'][1]}/" \
                    f"season/{season}/episode/{episode}"

        self.__s.headers.update({'referer': query_url})

    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Queries the search bar.

        :param query: The query string to pass.
        :return: A list of dictionaries, each dictionary containing the show ID and the show name.
                [{'id': '3284', 'name': 'בית הנייר / Money Heist'}, ... ]
        """
        return self.__s.get(f"{self.base}/ajax/index?search={query}").json()

    def urlEncode(self, query):
        return urllib.parse.quote(query)

    def findAll(self, text, startToken, endToken):
        cases = []
        while True:
            if text.find(startToken) == -1 or text.find(endToken) == -1:
                break
            try:
                text = text[text.find(startToken) + len(startToken):]
                key = text[: text.find(endToken)]
                cases.append(key)
            except:
                break
        return cases

    def getEpisodeCount(self):
        return len(self.findAll(self.__s.get(
            "https://sdarot{ext}/ajax/watch?episodeList={showID}&season={season}".format(ext=self.ext, showID=str(
                self.sidraData["SID"]), season=str(self.season))).text, 'data-episode="', '"'))

    def getData(self):
        csrfKey = self.__s.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
                                data={"preWatch": "true", "SID": str(self.sidraData["SID"]),
                                      "season": str(self.season), "ep": str(self.episode)}).text
        time.sleep(30)
        return json.loads(self.__s.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
                                        data={"watch": "false", "token": str(csrfKey),
                                              "serie": self.sidraData["SID"], "season": self.season,
                                              "episode": self.episode, "type": "episode"}).text)

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
