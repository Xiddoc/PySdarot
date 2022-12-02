import json
import os
import shutil
import time
import urllib
from typing import List

import requests

from SdarotController import SdarotController
from Show import Show


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
        resp = self.__s.get(f"{self.base}/ajax/index?search={query}")
        # Get output as class
        return [
            Show(show_id=show['id'], name=show['name'])
            for show in resp.json()
        ]

    # def urlEncode(self, query):
    #     return urllib.parse.quote(query)
    #
    # def getData(self):
    #     csrfKey = self.__s.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
    #                             data={"preWatch": "true", "SID": str(self.sidraData["SID"]),
    #                                   "season": str(self.season), "ep": str(self.episode)}).text
    #     time.sleep(30)
    #     return json.loads(self.__s.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
    #                                     data={"watch": "false", "token": str(csrfKey),
    #                                           "serie": self.sidraData["SID"], "season": self.season,
    #                                           "episode": self.episode, "type": "episode"}).text)
    #
    # def getURL(self):
    #     data = self.getData()
    #     maxQ = 0
    #     try:
    #         for quality in data["watch"]:
    #             if int(quality) > maxQ:
    #                 maxQ = int(quality)
    #     except KeyError:
    #         return False
    #     return "https://{serverName}/w/episode/{quality}/{vidID}.mp4?token={token}&time={time}".format(
    #         serverName=data["url"], quality=maxQ, vidID=data["VID"], token=data["watch"][str(maxQ)],
    #         time=str(data["time"]))
    #
    # def download_file(self, fileName):
    #     tempURL = self.getURL()
    #     if tempURL:
    #         try:
    #             with self.__s.get(tempURL, stream=True) as r:
    #                 with open(fileName, 'wb') as f:
    #                     try:
    #                         shutil.copyfileobj(r.raw, f)
    #                     except:
    #                         f.close()
    #                         os.remove(fileName)
    #                         return False
    #                     f.close()
    #                 r.close()
    #         except requests.exceptions.SSLError:
    #             return False
    #     else:
    #         return tempURL
