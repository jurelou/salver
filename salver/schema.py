schema_str = """
{
    "namespace": "salver.totazeo",
    "name": "Users",
    "type": "record",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "favorite_color", "type": "string"},
        {"name": "listof", "type": {"type": "array", "items": "string"}}
    ]
}

"""

class User(object):
    def __init__(self, name, favorite_color, listof):
        self.name = name
        self.favorite_color = favorite_color
        self.listof = listof


def user_to_dict(user, ctx):
    return dict(name=user.name,
                listof=user.listof,
                favorite_color=user.favorite_color)

def dict_to_user(obj, ctx):
    if obj is None:
        return None

    return User(name=obj['name'],
                listof=obj['listof'],
                favorite_color=obj['favorite_color'])