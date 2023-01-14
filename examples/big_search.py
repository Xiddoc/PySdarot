from pysdarot import PySdarot

# You have to manually update the TLD
s = PySdarot('.tw')

# Let's see if they have this show on their website
results = s.small_search("mo")

if not results:
    print("They don't have this show :(")
    exit()

# They do have the show! Let's show the options.
for i, result in enumerate(results):
    print(f"#{i} {result}")
