def get_name(event: dict) -> str:
    default_name = 'world'
    name: str

    if 'name' in event:
        return name
    else:
        return default_name


def lambda_handler(event: dict, _context) -> dict:
    return {
        'hello': get_name(event)
    }
