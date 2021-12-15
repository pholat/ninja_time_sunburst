#!/usr/bin/python3

from __future__ import annotations
from dataclasses import dataclass
import json
import plotly.express as px
import plotly.graph_objects as go
from typing import Union, List
from treelib import Tree, Node


def load(name):
    with open(name) as f:
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
    import argparse
    parser = argparse.ArgumentParser(description='generate sunburst of file')
    parser.add_argument('--file', dest='file', help='json file to load', required=True)
    args = parser.parse_args()

    root = Tree()
    total = root.create_node('total', 'total', data=Data())

    def keygen(x: List[str], y):
        return '|'.join(x[:y + 1])

    # load targets to nodes
    for val in load(args.file):
        el = Entry(**val)
        if ' ' in el.name:
            # NOTE ignore targets with ` ` in name
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

    data = {"ids": [], "labels": [], "parents": [], "values": []}
    for node in root.expand_tree():
        node = root[node]
        label = node.identifier.split('|')[-1]
        id = node.identifier
        pre = root.parent(node.identifier)
        parent = pre.identifier if pre is not None else ""
        value = node.data.data if type(node.data.data) is int else node.data.data.dur
        data["labels"].append(label)
        data["ids"].append(id)
        data["parents"].append(parent)
        data["values"].append(value)

    fig = go.Figure(go.Sunburst(**data))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.show()
