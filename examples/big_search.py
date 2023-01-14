from pysdarot import PySdarot

# You have to manually update the TLD
s = PySdarot('.tw')

# Large query
results = s.search("mo")

if not results:
    print("They don't have this show :(")
    exit()

print(f"We found {len(results)} shows.")
