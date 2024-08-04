# Advisor Watch

Yet another Resident Advisor scraper. Set a list of areas and a list of genres, and be notified whenever a new event pops up via Discord.

Can be run as a command-line utility or via Docker. For a list of valid genres, see genres.txt.

## Setup (Docker)

1. Edit compose.yaml with your desired settings. If AW_COUNTRY is set, ALL regions from that country will be watched, and AW_AREAS will be ignored.

## Usage (Docker)

`docker compose up --build -d`

## Installation (CLI)

`pip install .`

## Usage (CLI)

`advisor-watch --area "new york" --area "los angeles" --genre "jungle"`

If --country is set, ALL regions from that country will be watched, and any --area option will be ignored. By default, the state file lives in ~/advisor_watch.json.