#!/usr/bin/env python
import sys
import click
from os.path import expanduser, join, isfile
from loguru import logger
import json
import time

from ra_scrape.graphql import (
    get_events,
    get_area_ids_by_country,
    get_area_ids_by_areas,
    get_countries,
)
from advisor_watch.discord import send_alert


class AWType(click.types.ParamType):
    """
    Custom type so that splitting is done on commas
    """

    envvar_list_splitter = ","


@click.command()
@click.option("areas", "--area", multiple=True, type=AWType(), envvar="AW_AREAS")
@click.option("genres", "--genre", multiple=True, type=AWType(), envvar="AW_GENRES")
@click.option("country", "--country", envvar="AW_COUNTRY")
@click.option(
    "sleep_duration", "--sleep-duration", default=3600, envvar="AW_SLEEP_DURATION"
)
@click.option("state_file", "--state-file", envvar="AW_STATE_FILE")
@click.option("discord_webhook_url", "--discord-url", envvar="AW_DISCORD_WEBHOOK_URL")
def run(areas, genres, country, sleep_duration, state_file, discord_webhook_url):
    if not discord_webhook_url:
        sys.exit("Discord Webhook URL required")
    areas = [area.strip() for area in areas]
    genres = [genre.strip() for genre in genres]

    if not state_file:
        state_file = join(expanduser("~"), "advisor_watch.json")

    if isfile(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            already_alerted = json.load(f)
    else:
        already_alerted = []

    all_countries = get_countries()
    while True:
        if country:
            area_ids = get_area_ids_by_country(country, all_countries)
        else:
            area_ids = get_area_ids_by_areas(areas, all_countries)

        for event in get_events(area_ids=area_ids, genres=genres):
            if event["id"] in already_alerted:
                continue
            logger.info(f"Found a new event: {event['id']}")
            send_alert(discord_webhook_url=discord_webhook_url, event=event)
            already_alerted.append(event["id"])
            # Sleep a little so we don't spam Discord
            time.sleep(1)

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(already_alerted, f)
        logger.info("Sleeping")
        time.sleep(sleep_duration)


if __name__ == "__main__":
    run(auto_envvar_prefix="AW")
