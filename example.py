from sdarot import Sdarot

# You have to manually update the TLD
s = Sdarot('.tw')

# Let's see if they have this show on their website
results = s.search("money heist")

if results:
    # They do have the show! Let's get it's ID
    show_id = results[0]['id']
else:
    print("They don't have this show :(")
    exit()

# Now that we have the show ID, we can download it!
s.download_show(show_id, season=1, episode=1)
