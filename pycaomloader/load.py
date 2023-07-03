"""Main code to load CAOM observations"""

# pylint: disable=redefined-outer-name, protected-access, invalid-name

import os
from typing import Any
from datetime import datetime
from sqlalchemy import create_engine, text, Engine, DDL, event
from sqlalchemy.orm import Session
from caom2.observation import Observation
from caom2.plane import Plane, Position, Time, Energy, Metrics, Polarization, CustomAxis
from caom2.artifact import Artifact
from caom2.shape import Point, Circle, Polygon, Interval
from caom2.obs_reader_writer import ObservationReader
from sqlalchemy_utils.functions import database_exists, create_database
from pycaomloader.schema import Base, CaomObservation, CaomPlane


def load_engine(connection_string: str) -> Engine:
    """Create SQLAlchemy engine"""

    engine = create_engine(connection_string)

    # Special handling for sqlite
    if 'sqlite' in connection_string:
        engine = create_engine('sqlite://')
        conn = engine.connect()
        db_name = connection_string.replace('sqlite://', '')
        conn.execute(text(f"ATTACH DATABASE '{db_name[1:]}' as 'caom2'"))

    return engine


def prepare_database(connection_string: str,
                    drop_tables: bool = False
                    ):
    """Create the database tables"""

    # Create it if not already present
    if not database_exists(connection_string):
        create_database(connection_string)

    engine = load_engine(connection_string)

    base = Base  # this comes from schema.py
    base.metadata.bind = engine

    if drop_tables:
        base.metadata.drop_all(bind=engine)

    # Logic for ensuring caom2 schema exists first (not applicable for sqlite)
    if 'sqlite' not in connection_string:
        event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS caom2"))
    base.metadata.create_all(engine)


def store_items(field_items: dict, k: str, v: Any):
    """Helper function to get sub items from CAOM"""

    # print(k, v, type(v))

    # Exit early if None
    if v is None:
        field_items[k] = v
        return
    
    # Loop over child attributes to set them
    for k2, v2 in vars(v).items():
        # print(k, k2, v2, type(v2))
        if k2.endswith('points') or k2.endswith('samples'):
            # TODO: Figure out how to implement these
            continue
        elif isinstance(v2, (Point, Circle, Polygon, Interval, Position, Time, \
                           Energy, Metrics, Polarization, CustomAxis)) \
                            or k2.endswith('bounds'):
            # Recursive check to drill down into members
            store_items(field_items, k+k2, v2)
        elif isinstance(v2, (str, int, float, type(None), bool, datetime)):
            field_items[k+k2] = v2
        elif isinstance(v2, (set, list)):
            temp = ' | '.join([x for x in v2])
            if temp.strip() != '':
                # Don't store empty strings
                field_items[k+k2] = temp


def special_handling(field_items: dict, k: str, v: Any):
    """Special handling of certain fields"""

    if k in ('target', 'targetPosition', 'proposal', 'telescope', 'environment', 'instrument', \
             'provenance', 'position', 'time', 'energy', 'metrics', 'polarization', 'custom') \
            and v is not None:
        store_items(field_items, k, v)
    elif k in ('intent') and v is not None:
        # SQL validation not properly capturing just the value so have to set it here
        field_items[k] = v.value
    elif k in ('planes', 'artifacts'):
        # Handled separately
        return
    elif k == 'members':
        # TODO: Figure out how to handle members
        return
    elif k.endswith('read_groups'):
        # TODO: Figure out how to handle read groups
        return
    elif 'checksum' in k.lower() or 'uri' in k.lower():
        # Handle checksum/uri fields
        field_items[k] = v.uri
    else:
        field_items[k] = v


def rename_fields(k: str) -> str:
    """Helper function to rename some fields"""

    if k=='target_position':
        k = 'targetPosition'

    return k


def ingest_observation(file_name: str, 
                       connection_string: str):
    """Ingest an observation from an xml file"""

    # CAOM object
    obs = ObservationReader().read(source=file_name)

    # Prepare database objects
    db_objects = process_observation(obs)

    # Ingest into data
    engine = load_engine(connection_string)
    with Session(engine) as session:
        session.add_all(db_objects)
        session.commit()


def process_observation(obs: Observation) -> list:
    """Generate database objects for the observation"""

    # Database Objects
    db_objects = []
    db_obs = CaomObservation()

    # Loop over attributes of obs
    field_items = {}
    for k, v in vars(obs).items():
        if k == '_planes':
            # Generate plane database objects
            for _, plane in v.items():
                db_plane = process_plane(plane, obs.collection, obs.observation_id, obs._id)
                db_objects.append(db_plane)

        # strip starting _ for simplicity
        if k.startswith('_'):
            k = k[1:]
        # rename some fields
        k = rename_fields(k)

        # Special handling
        special_handling(field_items, k, v)

    # Set the type code based on whether this is Derived or Simple
    if 'Derived' in obs.__class__.__name__ or 'Composite' in obs.__class__.__name__:
        db_obs.typeCode = 'D'
    else:
        db_obs.typeCode = 'S'

    # Map to schema
    for k, v in field_items.items():
        setattr(db_obs, k, v)

    print(db_obs)
    db_objects.insert(0, db_obs)
    return db_objects


def process_plane(plane: Plane, collection: str, observation_id: str, observation_uri: str):
    """Generate database objects for the plane"""

    db_plane = CaomPlane()

    # Loop over attributes of obs
    field_items = {}
    for k, v in vars(plane).items():
        if k == '_artifacts':
            # TODO: Implement artifacts later
            pass

        # strip starting _ for simplicity
        if k.startswith('_'):
            k = k[1:]

        # Special handling
        special_handling(field_items, k, v)

    # Set some extra, required fields
    field_items['planeURI'] = f"caom:{collection}/{observation_id}/{plane.product_id}"
    field_items['obsID'] = observation_uri

    # Map to schema
    for k, v in field_items.items():
        setattr(db_plane, k, v)

    print(db_plane)

    return db_plane


def process_artifact(artifact: Artifact):
    pass


if __name__ == '__main__':  # pylint: disable=invalid-name

    # connection_string = 'postgresql+psycopg2://localhost:5432/caom'
    connection_string = 'sqlite:///caom.db'

    # Create database
    CREATE = True
    if CREATE:
        if 'sqlite' in connection_string and os.path.exists('caom.db'):
            os.remove('caom.db')
        prepare_database(connection_string)

    # Ingest XML
    file_name = 'pycaomloader/data/hst_11975_39_wfpc2_wfpc2_f170w_ubai390a.xml'
    ingest_observation(file_name, connection_string)

    # my_path = '../../data/CAOM/pyCAOM2/unittests/data/xml/'
    # for f in os.listdir(my_path):
    #     if f.endswith('.xml'):
    #         print(f'Ingesting {f}')
    #         ingest_observation(os.path.join(my_path, f), connection_string)
