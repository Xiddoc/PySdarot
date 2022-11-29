from sdarot import Sdarot


def download(show, season, episode):
    try:
        s = Sdarot(show, season, episode)
        if s.getEpisodeCount():
            s.downloadFile("{name}{season}_{episode}.mp4".format(name=show.strip().replace(" ", "_"), season=season,
                                                                 episode=episode))
    except:
        return False


download(show="money heist", season=1, episode=1)
