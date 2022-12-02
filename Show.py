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
        resp =

    def get_episode_count(self, season: int):
        return len(self.findAll(self.__s.get(
            "https://sdarot{ext}/ajax/watch?episodeList={showID}&season={season}".format(ext=self.ext, showID=str(
                self.sidraData["SID"]), season=str(self.season))).text, 'data-episode="', '"'))


    def download_show(self, show_id: id, season: int, episode: int):
        # We need to get the show metadata first so we can build the download URL
        sidra_data = self.search(show)



        query_url = f"{self.base}/watch/" \
                    f"{sidra_data['SID']}-{self.urlEncode(sidra_data['Sname'][0])}-{sidra_data['Sname'][1]}/" \
                    f"season/{season}/episode/{episode}"

        self.__s.get(query_url)