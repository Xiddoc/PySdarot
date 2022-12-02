from pysdarot import PySdarot

# You have to manually update the TLD
s = PySdarot('.tw')

# Let's see if they have this show on their website
results = s.search("money heist")

if not results:
    print("They don't have this show :(")
    exit()

# Yay, they have it!
my_show = results[0]

# Let's see what this show offers...
seasons = my_show.get_season_count()
print(f"Season count: {seasons}")

for i in range(1, seasons + 1):
    print(f"Episodes in season #{i}: {my_show.get_episode_count(i)}")
