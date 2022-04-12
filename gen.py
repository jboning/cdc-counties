#!/usr/bin/env python3

import itertools
import os
import requests

DATA_URL = "https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_external_data"

def fname(state):
    return f"states/{state.lower().replace(' ', '_')}.md"

def output(state, counties):
    counties = sorted(counties, key=lambda x: x["County"])
    with open(fname(state), "w") as f:
        f.write("State | County | Last Updated | Status\n")
        f.write("--- | --- | --- | --- \n")
        for c in counties:
            county = c["County"]
            date = c["report_date"]
            transmission = c["community_transmission_level"] or "(missing)"
            community_level = {
                0: "low",
                1: "medium",
                2: "high",
            }.get(c["CCL_community_burden_level_integer"], "(missing)")
            f.write(f"{state} | {county} | {date} | Community Level: {community_level}<br/>Community Transmission: {transmission}\n")

def process(data):
    data = data['integrated_county_latest_external_data']
    keyfunc = lambda x: x["State_name"]
    data = sorted(data, key=keyfunc)
    states = []
    for state, counties in itertools.groupby(data, keyfunc):
        states.append(state)
        output(state, counties)
    with open("index.md", "w") as f:
        for state in states:
            f.write(f" * [{state}]({fname(state)})\n")

def main():
    result = requests.get(DATA_URL)
    with open("data.json", "wb") as f:
        f.write(result.content)
    process(result.json())

if __name__ == "__main__":
    main()
