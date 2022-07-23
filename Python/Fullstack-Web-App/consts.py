import os

CHOICES = []
for i in range(1, 61): CHOICES.append(i)
CHOICES.append("All")

NEW_CONDITION = "&rt=nc&LH_ItemCondition=3"
LOCATION_US = "&rt=nc&LH_PrefLoc=3"
GOOGLE_SEARCH = f"https://www.google.com/search?q="
AMAZON_PREFIX = 'https://www.amazon.com'
KEEPALIVE_INTERVAL = 5

hostname = os.popen('hostname').read().replace('\n', '')
LOCAL_RUN = (hostname == "dev-machine")
