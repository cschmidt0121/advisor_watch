import requests
from ra_scrape.templates import get_events_query, get_all_countries_query


def get_events(area_ids: list[int], genres: list[str]):
    headers = {
        "Referer": "https://ra.co/events/us/newyorkcity",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "*/*",
    }

    page = 1
    processed = 0
    while True:
        query = get_events_query(page=page, area_ids=area_ids, genres=genres)

        r = requests.post(
            "https://ra.co/graphql", json=query, headers=headers, timeout=30
        )
        r.raise_for_status()

        j = r.json()

        eventListings = j["data"]["eventListings"]

        for event in eventListings["data"]:
            yield event['event']
            processed += 1

        if processed >= eventListings["totalResults"]:
            break

        page += 1

def get_countries():
    headers = {
        "Referer": "https://ra.co/events/us/newyorkcity",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "*/*",
    }

    query = get_all_countries_query()

    r = requests.post("https://ra.co/graphql", json=query, headers=headers, timeout=30)
    r.raise_for_status()

    j = r.json()

    countries = j["data"]["countries"]

    return countries

def get_area_ids_by_country(country_name: str, all_countries: dict):
    """
    Given a country name, find all area IDs contained within.
    Country name can be either the full name (United States of America),
    or the urlCode (US).
    """
    match = None
    for country in all_countries:
        if (
            country.get("name") == country_name
            or country.get("urlCode") == country_name
        ):
            match = country
            break

    if not match:
        raise IndexError(f"Could not find country with name {country_name}")

    # Area IDs are returned a string for some reason
    return [int(area["id"]) for area in match['areas']]

def get_area_ids_by_areas(areas: list[str], all_countries: dict):
    """
    Given a list of area names, return a list of area ids
    """
    out = []
    for country in all_countries:
        for area in country['areas']:
            if area["name"] in areas or area["urlName"] in areas:
                out.append(int(area["id"]))

            for subregion in area.get("subregion", []):
                if subregion["name"] in areas or subregion["urlName"] in areas:
                    out.append(int(subregion["id"]))

    # Deduplicate
    out = list(set(out))

    return out