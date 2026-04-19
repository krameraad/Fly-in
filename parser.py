import sys
from pathlib import Path
from typing import Any

from lark import Lark, Transformer

from zone import ZoneType
from formatting import X, Y


class ParsingError(Exception):
    pass


class TreeToMap(Transformer):
    @staticmethod
    def _validate_metadata(metadata: dict[str, str | int]):
        expected = {'color', 'max_drones', 'zone', 'max_link_capacity'}
        unexpected = set(metadata.keys()) - expected
        if unexpected:
            raise ParsingError(f'Unexpected metadata {unexpected}.')

        zonetype = metadata.pop('zone', None)
        if zonetype:
            try:
                metadata['zonetype'] = ZoneType[zonetype.upper()]
            except KeyError:
                print(
                    f'{Y}Warning: Unexpected zone type "{zonetype}".{X}',
                    file=sys.stderr
                )
                metadata['zonetype'] = ZoneType.NORMAL
        return metadata

    def NAME(self, token):
        return str(token)

    def INT(self, token):
        return int(token)

    def key(self, items):
        return items[0]

    def value(self, items):
        return items[0]

    def pair(self, items):
        key, value = items
        return (key, value)

    def metadata(self, items):
        return dict(items)

    def start_hub(self, items):
        name, x, y, *meta = items
        metadata = self._validate_metadata(meta[0]) if meta else {}
        if 'zonetype' not in metadata:
            metadata['zonetype'] = ZoneType.START
        return ("start_hub", {"name": name, "x": x, "y": y} | metadata)

    def end_hub(self, items):
        name, x, y, *meta = items
        metadata = self._validate_metadata(meta[0]) if meta else {}
        if 'zonetype' not in metadata:
            metadata['zonetype'] = ZoneType.END
        return ("end_hub", {"name": name, "x": x, "y": y} | metadata)

    def hub(self, items):
        name, x, y, *meta = items
        metadata = self._validate_metadata(meta[0]) if meta else {}
        return ("hub", {"name": name, "x": x, "y": y} | metadata)

    def connection(self, items):
        a, b, *meta = items
        metadata = meta[0] if meta else {}
        metadata = metadata.get('max_link_capacity', 1)
        return ("link", {'hubs': (a, b), 'max_link_capacity': metadata})

    def nb_drones(self, items):
        return ("nb_drones", items[0])

    def start(self, items):
        result: dict[str, int | dict | list] = {
            "nb_drones": None,
            "start_hub": None,
            "end_hub": None,
            "hubs": [],
            "links": []
        }
        for item in items:
            match item[0]:
                case "nb_drones":
                    result["nb_drones"] = item[1]
                case "start_hub":
                    result["start_hub"] = item[1]
                case "end_hub":
                    result["end_hub"] = item[1]
                case "hub":
                    result["hubs"].append(item[1])
                case "link":
                    result["links"].append(item[1])
        return result


def parse(filename: Path) -> dict[str, Any]:
    """Parse map data from a file.

    Args:
        filename: Path to read from.

    Returns:
        Dictionary containing data to be used for building the map.
        All hubs are given as dictionaries, and can be unpacked
        to build the hub objects (`Zone(**hub)`).

        Links/connections are tuples of `(from, to, capacity)`.
        - `nb_drones` - Number of drones.
        - `start_hub` - Starting hub.
        - `end_hub` - End hub.
        - `hubs` - List of hubs, excluding start and end hubs.
        - `links` - List of links.

    Raises:
        LarkError: When the input map file contains syntax errors.
        ParsingError: When the input map file contains semantic errors.
    """

    grammar = r"""
start: line+

?line: nb_drones
     | start_hub
     | end_hub
     | hub
     | connection

nb_drones: "nb_drones:" INT
start_hub: "start_hub:" NAME INT INT metadata?
end_hub: "end_hub:" NAME INT INT metadata?
hub: "hub:" NAME INT INT metadata?
connection: "connection:" NAME "-" NAME metadata?

metadata: "[" pair+ "]"

key: NAME
value: NAME | INT
pair: key "=" value

NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
INT: /-?\d+/

COMMENT: /#[^\n]*/

%import common.WS
%ignore WS
%ignore COMMENT
    """

    map_parser = Lark(grammar, parser='lalr', transformer=TreeToMap())
    with filename.open("r", encoding="utf-8") as file:
        tree = map_parser.parse(file.read())

        # Checking that critical data is supplied.
        missing = {x for x in tree if tree[x] is None}
        if missing:
            raise ParsingError(f'Critical map data is missing: {missing}.')

        # Checking that links connect to valid hubs.
        all_hubs = [x['name'] for x in tree['hubs']] \
            + [tree['start_hub']['name'], tree['end_hub']['name']]
        for link in tree['links']:
            if link['hubs'][0] not in all_hubs \
                    or link['hubs'][1] not in all_hubs:
                raise ParsingError(
                    f'Link "{"-".join(link['hubs'])}'
                    'connects to an invalid hub.')

        return tree
