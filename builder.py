from zone import Zone


def build(data: dict) -> dict[str, Zone]:
    start_hub = Zone(**data['start_hub'])
    end_hub = Zone(**data['end_hub'])
    zones: dict[str, Zone] = {x['name']: Zone(**x) for x in data['hubs']}
    zones.update({start_hub.name: start_hub, end_hub.name: end_hub})

    for link in data['links']:
        zones[link[0]].links.append((zones[link[1]], link[2]))
        zones[link[1]].links.append((zones[link[0]], link[2]))
    return zones
