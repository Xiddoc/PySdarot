#!/usr/bin/env python
# coding: utf-8

import requests
import urllib
import time
import json
import shutil
import os


class Sdarot:
    def __init__(self, sidra, season, episode):
        self.ext = ".tv"
        self.session = requests.Session()
        self.session.headers.update({
            'authority': 'sdarot{ext}'.format(ext=self.ext),
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://sdarot{ext}'.format(ext=self.ext),
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en;q=0.9,en-CA;q=0.8,he;q=0.7',
        })
        self.sidra = sidra
        self.sidraData = self.search(self.sidra)
        if not self.sidraData:
            raise ConnectionError
        self.season = season
        self.episode = episode
        self.session.headers.update({'referer': "https://sdarot{}/watch/{}-{}-{}/season/{}/episode/{}".format(
            str(self.ext), str(self.sidraData["SID"]), self.urlEncode(self.sidraData["Sname"][0]),
            str(self.sidraData["Sname"][1]), str(self.season), str(self.episode))})

    def search(self, query):
        try:
            retData = "VID" + self.findAll(
                self.session.get("https://sdarot{}/search?term={}".format(self.ext, self.urlEncode(query))).text,
                '<script type="text/javascript">\nvar VID', '</script>')[0]
        except:
            return False
        convData = retData.replace("\t", "") \
                       .replace("var ", "") \
                       .replace(";", ",") \
                       .replace("=", " : ") \
                       .replace("'", "\"").strip()[:-1]
        lines = []
        for line in convData.splitlines():
            l = line.strip().split(":")
            lines.append('"' + l[0].strip() + '" : ' + ":".join(l[1:]).strip())
        jsData = "{" + "\n".join(lines) + "}"
        return json.loads(jsData)

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
        return len(self.findAll(self.session.get(
            "https://sdarot{ext}/ajax/watch?episodeList={showID}&season={season}".format(ext=self.ext, showID=str(
                self.sidraData["SID"]), season=str(self.season))).text, 'data-episode="', '"'))

    def getData(self):
        csrfKey = self.session.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
                                    data={"preWatch": "true", "SID": str(self.sidraData["SID"]),
                                          "season": str(self.season), "ep": str(self.episode)}).text
        time.sleep(30)
        return json.loads(self.session.post("https://sdarot{ext}/ajax/watch".format(ext=self.ext),
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

    def downloadFile(self, fileName):
        tempURL = self.getURL()
        if tempURL:
            try:
                with self.session.get(tempURL, stream=True) as r:
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
