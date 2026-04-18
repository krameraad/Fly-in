from pathlib import Path
from typing import Any

from zone import ZoneType


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
        RuntimeError: When the input map file contains mistakes.
    """
    def parse_hub_metadata(pairs: list[str]) -> dict[str, Any]:
        "Parse information for hub metadata."
        result = {}
        for pair in pairs:
            k, v = pair.split('=')
            match k:
                case 'zone':
                    result.update({'zonetype': ZoneType[v.upper()]})
                case 'color':
                    result.update({'color': v})
                case 'max_drones':
                    result.update({'max_drones': int(v)})
                case _:
                    raise RuntimeError(f'Invalid metadata {(k, v)} in map.')
        return result

    def parse_hub(s: str) -> dict[str, Any]:
        "Parse information for building a hub."
        result = {}
        info = s.split(maxsplit=3)
        result['name'] = info[0]
        result['x'], result['y'] = int(info[1]), int(info[2])
        if len(info) > 3:
            result.update(parse_hub_metadata(info[3].strip('[]').split()))
        return result

    def parse_link(s: str) -> tuple[str, str, int]:
        "Parse information for connecting two hubs."
        info = s.split(maxsplit=1)
        max_link_capacity = 1
        if len(info) > 1:
            max_link_capacity = int(info[1].strip('[]').split('=')[1])
        return tuple(info[0].split('-') + [max_link_capacity])

    data: dict[str, Any] = {}
    with filename.open("r", encoding="utf-8") as file:
        hubs: list[dict[str, Any]] = []
        links: list[tuple[str, str, int]] = []

        for i, raw_line in enumerate(file, start=1):
            line = raw_line.strip()

            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                raise RuntimeError(f"Invalid line format at line {i}.")

            key, value = line.split(":", maxsplit=1)
            key, value = key.strip(), value.strip()
            match key:
                case 'nb_drones':
                    data['nb_drones'] = int(value)
                case 'start_hub':
                    h = parse_hub(value)
                    if not h.get('zonetype'):
                        h['zonetype'] = ZoneType.START
                    data['start_hub'] = h
                case 'end_hub':
                    h = parse_hub(value)
                    if not h.get('zonetype'):
                        h['zonetype'] = ZoneType.END
                    data['end_hub'] = h
                case 'hub':
                    hubs.append(parse_hub(value))
                case 'connection':
                    links.append(parse_link(value))

        all_hubs = [x['name'] for x in hubs] \
            + [data['start_hub']['name']] + [data['end_hub']['name']]
        for link in links:
            if link[0] not in all_hubs or link[1] not in all_hubs:
                raise RuntimeError(
                    f'Link "{"-".join(link[:2])}" connects to an invalid hub.')

        data['hubs'] = hubs
        data['links'] = links

    return data
