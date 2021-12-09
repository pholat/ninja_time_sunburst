#!/usr/bin/python3

from dataclasses import dataclass
import re
import json
import plotly.express as px

def load():
    with open("lol.json") as f:
        return json.load(f)


@dataclass
class entry:
    name: str
    cat: str
    ph: str
    ts: int
    dur: int
    pid: int
    tid: int
    args: dict


@dataclass
class group:
    name: str
    values: list[entry]
    timetotal: int


if __name__ == "__main__":
    timings = {}
    regexp = re.compile(r"^module-(apps|services)/([A-Za-z\-]*)/.*")

    for val in load():
        el = entry(**val)
        if ' ' in el.name:
            # WIP ignore shitty targets with ` ` in name
            continue
        name = regexp.match(el.name)
        if name is not None:
            g = name.group(2)
            if g not in timings:
                timings[g] = group(g, [], 0)
            timings[g].values.append(el)
            timings[g].timetotal = timings[g].timetotal + el.dur
    for key, val in sorted(timings.items(), key=lambda x: x[1].timetotal):
        print(f"{key} : {val.timetotal/1000000 : ^16}")
        for el in sorted(val.values, key=lambda x: x.dur):
            print(" " * 10 + f"{el.name.split('/')[-1]} time: {el.dur/1000000}")

    data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])
    fig =px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
    fig.show()
