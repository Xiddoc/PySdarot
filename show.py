#!/usr/bin/env python
# coding: utf-8

from sdarot import Sdarot
from threading import Thread
from time import sleep


def download(show, season, episode):
    try:
        s = Sdarot(show, season, episode)
        if s.getEpisodeCount():
            s.downloadFile("{name}{season}_{episode}.mp4".format(name=show.strip().replace(" ", "_"), season=season,
                                                                 episode=episode))
    except:
        return False


show = "money heist"

proc = download(show, season=1, episode=1)
exit(1)

procs = []
season = 1
for episode in range(7, 14):
    print("Downloading S{se}E{ep}...".format(se=season, ep=episode))
    proc = Thread(target=download, args=[show, season, episode])
    proc.setDaemon(True)
    proc.start()
    procs.append(proc)

# procs = []
# for season in range(1, 4 + 1):
# 	for episode in range(1, 13 + 1):
# 		print("Downloading S{se}E{ep}...".format(se = season, ep = episode))
# 		proc = Thread(target = download, args = [show, season, episode])
# 		proc.setDaemon(True)
# 		proc.start()
# 		procs.append(proc)
# 		sleep(5)
print("Working...")
for proc in procs:
    proc.join()
