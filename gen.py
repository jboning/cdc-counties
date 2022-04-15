#!/usr/bin/env python3

import itertools
import os
import requests

DATA_URL = "https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=integrated_county_latest_external_data"
STATE_ABBR = """
Alabama	AL
Alaska	AK
Arizona	AZ
Arkansas	AR
American Samoa	AS
California	CA
Colorado	CO
Commonwealth of the Northern Mariana Islands	MP
Connecticut	CT
Delaware	DE
District of Columbia	DC
Florida	FL
Georgia	GA
Guam	GU
Hawaii	HI
Idaho	ID
Illinois	IL
Indiana	IN
Iowa	IA
Kansas	KS
Kentucky	KY
Louisiana	LA
Maine	ME
Maryland	MD
Massachusetts	MA
Michigan	MI
Minnesota	MN
Mississippi	MS
Missouri	MO
Montana	MT
Nebraska	NE
Nevada	NV
New Hampshire	NH
New Jersey	NJ
New Mexico	NM
New York	NY
North Carolina	NC
North Dakota	ND
Northern Mariana Islands	CM
Ohio	OH
Oklahoma	OK
Oregon	OR
Pennsylvania	PA
Puerto Rico	PR
Rhode Island	RI
South Carolina	SC
South Dakota	SD
Tennessee	TN
Texas	TX
Trust Territories	TT
Utah	UT
Vermont	VT
Virginia	VA
Virgin Islands	VI
Washington	WA
West Virginia	WV
Wisconsin	WI
Wyoming	WY
"""
STATE_ABBR_MAP = dict(line.rsplit(None, 1) for line in STATE_ABBR.strip().split("\n"))

def normalize(state):
    return state.lower().replace(' ', '_')

def fname(state):
    return f"states/{normalize(state)}.md"

def output(state, counties):
    counties = sorted(counties, key=lambda x: x["County"])
    state_abbr = STATE_ABBR_MAP.get(state, state)
    with open(fname(state), "w") as f:
        f.write("State | County | Status | Last Updated\n")
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
            f.write(f"{state_abbr} | {county} <a href=\"#{normalize(county)}\">#</a> | <a name=\"{normalize(county)}\"></a>Community Level: {community_level}<br/>Community Transmission: {transmission} | {date}\n")

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
