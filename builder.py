from zone import Zone


def build(data: dict) -> dict[str, Zone]:
    """Creates a dictionary containing all necessary objects for the map.
    """
    start_hub = Zone(**data['start_hub'])
    end_hub = Zone(**data['end_hub'])

    hubs: dict[str, Zone] = {x['name']: Zone(**x) for x in data['hubs']}
    hubs.update({start_hub.name: start_hub, end_hub.name: end_hub})

    for link in data['links']:
        hubs[link['hubs'][0]].links.append(
            (hubs[link['hubs'][1]], link['max_link_capacity']))
        hubs[link['hubs'][1]].links.append(
            (hubs[link['hubs'][0]], link['max_link_capacity']))
    return hubs
