import re
import requests
from cachetools import cached, LRUCache, TTLCache

# Cache as much as possible to avoid being an asshole
@cached(cache=TTLCache(maxsize=1024, ttl=86400))
def get_venue_address(venue_id: int):
    """
    Grabs a venue page and parses out the address.
    There is almost certainly a better way to get this, maybe even with GraphQL?
    """
    headers = {
        "Referer": "https://ra.co/events/us/newyorkcity",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    
    r = requests.get(f"https://ra.co/clubs/{venue_id}", headers=headers)
    if r.status_code == 404:
        return ""
    r.raise_for_status()

    
    matches = re.findall(r'"Venue:\d+":{"id":"\d+".*"address":"([^\"]+)"', r.text)

    if not matches:
        return ""
    return matches[0]