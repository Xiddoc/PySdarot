from pysdarot import PySdarot

# You will need a username and password to download episodes
s = PySdarot(
    sdarot_tld='.tw',
    username=input("Username > "),
    password=input("Password > ")
)

# Let's get this show's pilot/first episode
results = s.small_search("money heist")

# First result of the search results
my_show = results[0]

# Get the episode
print("Downloading episode...")
my_show.download_episode(season=1, episode=1, file_path="./my_episode.mp4")

