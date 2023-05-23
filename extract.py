"""Extract NEOs and approaches data from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided
at the command line, and uses the resulting collections to
build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import json
from typing import List
from collections import defaultdict
from csv import DictReader as reader

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path) -> List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing NEOs data.
    :return: A collection of `NearEarthObject`s.
    """
    parsed = dict()
    try:
        with open(neo_csv_path, encoding="UTF-8") as file:
            data = reader(file, delimiter=',')

            for row in data:
                pdes = row['pdes']
                neo = NearEarthObject(
                    name=row['name'],
                    designation=pdes,
                    hazardous=row['pha'],
                    diameter=row['diameter']
                )
                parsed[pdes.lower()] = neo
    except (OSError, IOError) as err:
        print(f'Error loading data from {neo_csv_path}')
        raise err

    return parsed


def load_approaches(cad_json_path) -> List[CloseApproach]:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # parsed = []
    mapped = defaultdict(list)
    try:
        with open(cad_json_path, encoding="UTF-8") as file:
            json_data = json.load(file)
            data = json_data['data']
            fields = json_data['fields']

            for record in data:
                pdes = record[fields.index('des')]
                cls_approach = CloseApproach(
                    designation=pdes,
                    time=record[fields.index('cd')],
                    distance=record[fields.index('dist')],
                    velocity=record[fields.index('v_rel')]
                )
                mapped[pdes.lower()].append(cls_approach)
                # parsed.append(cls_approach)

    except (OSError, IOError) as err:
        print(f'Error loading data from {cad_json_path}')
        raise err

    return mapped
