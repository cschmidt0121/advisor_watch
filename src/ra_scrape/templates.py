from datetime import datetime

def get_events_query(page: int, area_ids: list[int], genres: list[str]):
    """
    Build a GraphQL query to grab events for a list of genres and area IDs
    Pagination starts at 1.
    """
    if len(area_ids) == 1:
        area_query = {"eq": area_ids[0]}
    else:
        area_query = {"any": area_ids}

    if len(genres) == 1:
        genre_query = {"eq": genres[0]}
    else:
        genre_query = {"any": genres}

    return {
        "operationName": "GET_EVENT_LISTINGS",
        "variables": {
            "filters": {
                "areas": area_query,
                "listingDate": {"gte": datetime.now().strftime("%Y-%m-%d")},
                "genre": genre_query,
            },
            "filterOptions": {"genre": len(genres) > 0, "eventType": True},
            "pageSize": 20,
            "page": page,
            "sort": {
                "listingDate": {"order": "ASCENDING"},
                "score": {"order": "DESCENDING"},
                "titleKeyword": {"order": "ASCENDING"},
            },
        },
        "query": "query GET_EVENT_LISTINGS($filters: FilterInputDtoInput, $filterOptions: FilterOptionsInputDtoInput, $page: Int, $pageSize: Int, $sort: SortInputDtoInput) {\n  eventListings(\n    filters: $filters\n    filterOptions: $filterOptions\n    pageSize: $pageSize\n    page: $page\n    sort: $sort\n  ) {\n    data {\n      id\n      listingDate\n      event {\n        ...eventListingsFields\n        artists {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    filterOptions {\n      genre {\n        label\n        value\n        count\n        __typename\n      }\n      eventType {\n        value\n        count\n        __typename\n      }\n      location {\n        value {\n          from\n          to\n          __typename\n        }\n        count\n        __typename\n      }\n      __typename\n    }\n    totalResults\n    __typename\n  }\n}\n\nfragment eventListingsFields on Event {\n  id\n  date\n  startTime\n  endTime\n  title\n  contentUrl\n  flyerFront\n  isTicketed\n  attending\n  isSaved\n  isInterested\n  queueItEnabled\n  newEventForm\n  images {\n    id\n    filename\n    alt\n    type\n    crop\n    __typename\n  }\n  pick {\n    id\n    blurb\n    __typename\n  }\n  venue {\n    id\n    name\n    contentUrl\n    live\n    __typename\n  }\n  __typename\n}\n",
    }


def get_all_countries_query():
    return {
        "operationName": "GET_ALL_LOCATIONS_QUERY",
        "variables": {},
        "query": "query GET_ALL_LOCATIONS_QUERY {\n  countries {\n    id\n    name\n    urlCode\n    topCountry\n    order\n    areas {\n      id\n      name\n      isCountry\n      urlName\n      parentId\n      subregion {\n        id\n        name\n        urlName\n        country {\n          id\n          name\n          urlCode\n          __typename\n        }\n        __typename\n      }\n      country {\n        id\n        name\n        urlCode\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
    }
