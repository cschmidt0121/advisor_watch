import requests
from datetime import datetime
from ra_scrape.web import get_venue_address


def format_event(event: dict):
    link = f"https://ra.co{event['contentUrl']}"
    date_dt = datetime.fromisoformat(event["date"])
    date = date_dt.strftime("%m/%d/%Y")

    title = event["title"]
    venue_id = int(event["venue"]["id"])
    venue_address = get_venue_address(venue_id)
    venue_name = event["venue"]["name"]
    artists = [artist["name"] for artist in event.get("artists", [])]
    artist_str = "- " + "\n- ".join(artists) if len(artists) != 0 else ""
    if event.get("images"):
        flyer = event["images"][0]["filename"]
    else:
        flyer = ""

    message = f"""
# {title}

## {venue_name}
{venue_address}
{date}

{artist_str}
{link}
               """

    body = {"username": "The Dark Stranger", "content": message}

    if flyer:
        body["embeds"] = [{"image": {"url": flyer}}]

    return body


def send_alert(discord_webhook_url: str, event: dict):
    body = format_event(event)
    r = requests.post(discord_webhook_url, json=body)
    r.raise_for_status()
