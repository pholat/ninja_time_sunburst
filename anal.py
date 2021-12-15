#!/usr/bin/python3

from __future__ import annotations
from dataclasses import dataclass
import json
import plotly.express as px
from typing import Union, List
from treelib import Tree, Node


def load():
    with open("lol.json") as f:
        return json.load(f)


@dataclass
class Entry:
    name: str
    cat: str
    ph: str
    ts: int
    dur: int
    pid: int
    tid: int
    args: dict


class Data:
    def __init__(self):
        self.data: Union[Entry, int, None] = 0

    def setData(self, data):
        if type(data) not in [Entry, int, None]:
            raise RuntimeError(f"data should be either Entry, int or None, but is {type(data)}")
        self.data = data


if __name__ == "__main__":
    root = Tree()
    total = root.create_node('total', 'total', data=Data())

    def keygen(x: List[str], y):
        return '.'.join(x[:y + 1])

    # load targets to nodes
    for val in load():
        el = Entry(**val)
        if ' ' in el.name:
            # WIP ignore shitty targets with ` ` in name
            continue

        branches = el.name.split('/')
        previous = total

        for key, val in enumerate(branches):
            id = keygen(branches, key)
            if id in root:
                previous = root[id]
            else:
                previous = root.create_node(val, id, parent=previous, data=Data())
            if type(root[id].data.data) is Entry:
                print("something is wrong on {val} : {branches} : {el.name}")
            else:
                root[id].data.data = root[id].data.data + el.dur

    # print(root.to_json(with_data=False))

    data = {"character": [], "parent": [], "value": []}
    for node in root.expand_tree():
        node = root[node]
        character = node.identifier
        pre = root.parent(node.identifier)
        parent = pre.identifier if pre is not None else ""
        value = node.data.data if type(node.data.data) is int else node.data.data.dur
        # print("------------------------------")
        # print(f": {character} : {parent} : {value}")
        # print("------------------------------")
        data["character"].append(character)
        data["parent"].append(parent)
        data["value"].append(value)

    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
    fig.show()
