from zone import Zone


def build(data: dict) -> dict[str, Zone]:
    """Creates a dictionary containing all necessary objects for the map.
    """
    start_hub = Zone(**data['start_hub'])
    end_hub = Zone(**data['end_hub'])

    hubs: dict[str, Zone] = {x['name']: Zone(**x) for x in data['hubs']}
    hubs.update({start_hub.name: start_hub, end_hub.name: end_hub})

    for link in data['links']:
        hubs[link[0]].links.append((hubs[link[1]], link[2]))
        hubs[link[1]].links.append((hubs[link[0]], link[2]))
    return hubs
