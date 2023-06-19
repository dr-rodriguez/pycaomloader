# Main code to load CAOM observations

from typing import Any
from datetime import datetime
from caom2.shape import Point
from caom2.obs_reader_writer import ObservationReader
from schema import *


def create_database():
    # Create the database tables
    pass


def store_items(field_items: dict, k: str, v: Any):
    # Helper to get sub items from CAOM
    for k2, v2 in vars(v).items():
        # print(k, k2, v2, type(v2))
        if isinstance(v2, (str, int, float, type(None), bool, datetime)):
            field_items[k+k2] = v2
        if isinstance(v2, (set, list)):
            field_items[k+k2] = ' | '.join([x for x in v2])
        elif isinstance(v2, (Point)):
            store_items(field_items, k+k2, v2)


def rename_fields(k: str) -> str:
    # Helper function to rename some fields
    if k== 'target_position':
        k = 'targetPosition'

    return k


def ingest_observation(file_name: str):
    # Ingest the observations

    # CAOM object
    obs = ObservationReader().read(source=file_name)

    # Database Object
    db_obs = CaomObservation()

    # Loop over attributes of obs
    field_items = {}
    for k, v in vars(obs).items():
        if k == '_planes':
            # TODO: Figure out how to handle planes
            continue

        # strip starting _ for simplicity
        if k.startswith('_'):
            k = k[1:]
        # rename some fields
        k = rename_fields(k)

        # Special handling
        if k in ('target', 'targetPosition', 'proposal', 'telescope', 'environment', 'instrument'):
            store_items(field_items, k, v)
        elif k in ('intent'):
            # SQL validation not properly capturing just the value so have to set it here
            field_items[k] = v.value
        elif k == 'members':
            # TODO: Figure out how to handle members
            continue
        elif k == 'meta_read_groups':
            # TODO: Figure out how to handle read groups
            continue
        elif 'checksum' in k.lower() or 'uri' in k.lower():
            # Handle checksum/uri fields
            field_items[k] = v.uri
        else:
            field_items[k] = v

    # Map to schema
    for k, v in field_items.items():
        setattr(db_obs, k, v)

    print(db_obs)
        

if __name__ == '__main__':
    file_name = 'pycaomloader/data/hst_11975_39_wfpc2_wfpc2_f170w_ubai390a.xml'
    ingest_observation(file_name)
