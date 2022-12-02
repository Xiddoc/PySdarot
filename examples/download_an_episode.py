from pysdarot import PySdarot

# You have to manually update the TLD
s = PySdarot('.tw')

# Let's get this show's pilot/first episode
results = s.search("money heist")

# First result of the search results
my_show = results[0]

# Get the episode
print("Downloading episode...")
video = my_show.download_episode(season=1, episode=1)

# Write it to a file so we can watch it later
with open("episode.mp4", 'wb') as f:
    f.write(video)
