# python
import json
from os.path import dirname, join, exists
from com_hub import prefs


def get_resources():
    """Gets the resources directory.

    Returns:
        (str): The string path to the resources directory.
    """
    res_path = __file__
    # Go up to kit root
    for i in range(3):
        res_path = dirname(res_path)
    # Add the resources path
    prefs.resources = join(res_path, "resources")
    # Load the authors
    with open(join(prefs.resources, "authors.json"), "r") as author_file:
        prefs.authors = json.load(author_file)
    return prefs.resources


def load_resource(res_type):
    """Loads a given resource from the resources directory.

    Args:
        res_type (str): The resource type to load

    Returns:
        (dict): The loaded resource.
    """
    res_path = prefs.resources if prefs.resources else get_resources()

    resource = join(res_path, "{}.json".format(res_type))

    if exists(resource):
        with open(resource, "r") as resource_file:
            return json.load(resource_file)
    else:
        return None

get_resources()
