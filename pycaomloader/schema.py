"""Database Schema defined by SQLAlchemy"""

# pylint: disable=trailing-whitespace, line-too-long, unused-argument, unused-import

from datetime import datetime
from uuid import UUID

from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, Float, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, validates


metadata_obj = MetaData(schema="caom2")


class Base(DeclarativeBase):
    metadata = metadata_obj


# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#using-annotated-declarative-table-type-annotated-forms-for-mapped-column
# default type mapping, deriving the type for mapped_column()
# from a Mapped[] annotation
# type_map: Dict[Type[Any], TypeEngine[Any]] = {
#     bool: types.Boolean(),
#     bytes: types.LargeBinary(),
#     datetime.date: types.Date(),
#     datetime.datetime: types.DateTime(),
#     datetime.time: types.Time(),
#     datetime.timedelta: types.Interval(),
#     decimal.Decimal: types.Numeric(),
#     float: types.Float(),
#     int: types.Integer(),
#     str: types.String(),
#     uuid.UUID: types.Uuid(),
# }

class CaomCommon:
    """Common columns for all CAOM Tables"""

    last_modified: Mapped[Optional[datetime]] = mapped_column('lastModified')  # caom2:Observation.lastModified	timestamp	
    max_last_modified: Mapped[Optional[datetime]] = mapped_column('maxLastModified')  # caom2:Observation.maxLastModified	timestamp	
    meta_checksum: Mapped[Optional[str]] = mapped_column('metaChecksum')  # caom2:Observation.metaChecksum	uri	
    acc_meta_checksum: Mapped[Optional[str]] = mapped_column('accMetaChecksum')  # caom2:Observation.accMetaChecksum	uri	


class CaomObservation(CaomCommon, Base):
    """Observation Table"""

    __tablename__ = "Observation"

    # Some attribute names are different from the DB names
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#using-descriptors-and-hybrids

    uri: Mapped[str] = mapped_column('observationURI', String)  # caom2:Observation.uri	uri	indexed
    id: Mapped[UUID] = mapped_column('obsID', primary_key=True)	# caom2:Observation.id	uuid	indexed
    collection: Mapped[str] = mapped_column(String(32))  # caom2:Observation.collection		indexed
    observation_id: Mapped[str] = mapped_column('observationID', String(128))  # caom2:Observation.observationID		indexed
    algorithm: Mapped[Optional[str]] = mapped_column('algorithm_name', String(32))  # caom2:Observation.algorithm.name
    type: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.type		
    intent: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.intent		
    sequence_number: Mapped[Optional[int]] = mapped_column('sequenceNumber', Integer)  # caom2:Observation.sequenceNumber		
    meta_release: Mapped[Optional[datetime]] = mapped_column('metaRelease')  # caom2:Observation.metaRelease	timestamp	
    meta_read_groups: Mapped[Optional[str]] = mapped_column('metaReadGroups')   # caom2:Observation.metaReadGroups		
    proposal_id: Mapped[Optional[str]] = mapped_column(String(128))  # caom2:Observation.proposal.id		indexed
    proposal_pi: Mapped[Optional[str]] = mapped_column(String(128))  # caom2:Observation.proposal.pi		
    proposal_project: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.proposal.project		
    proposal_title: Mapped[Optional[str]] = mapped_column(String(256))  # caom2:Observation.proposal.title		
    proposal_keywords: Mapped[Optional[str]]  # caom2:Observation.proposal.keywords		
    target_name: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.target.name		
    target_targetID: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.target.targetID	uri	
    target_type: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.target.type		
    target_standard: Mapped[Optional[bool]]  # caom2:Observation.target.standard		
    target_redshift: Mapped[Optional[float]]  # caom2:Observation.target.redshift		
    target_moving: Mapped[Optional[bool]]  # caom2:Observation.target.moving		
    target_keywords: Mapped[Optional[str]]  # caom2:Observation.target.keywords		
    targetPosition_coordsys: Mapped[Optional[str]] = mapped_column(String(16))  # caom2:Observation.targetPosition.coordsys		
    targetPosition_coordinates_cval1: Mapped[Optional[float]] # caom2:Observation.targetPosition.coordinates.cval1		
    targetPosition_equinox: Mapped[Optional[float]] # caom2:Observation.targetPosition.equinox		
    targetPosition_coordinates_cval2: Mapped[Optional[float]] # caom2:Observation.targetPosition.coordinates.cval2		
    telescope_name: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.telescope.name		
    telescope_geo_location_x: Mapped[Optional[float]] = mapped_column('telescope_geoLocationX', Float)  # caom2:Observation.telescope.geoLocationX		
    telescope_geo_location_y: Mapped[Optional[float]] = mapped_column('telescope_geoLocationY', Float)  # caom2:Observation.telescope.geoLocationY		
    telescope_geo_location_z: Mapped[Optional[float]] = mapped_column('telescope_geoLocationZ', Float)  # caom2:Observation.telescope.geoLocationZ		
    telescope_keywords: Mapped[Optional[str]]  # caom2:Observation.telescope.keywords		
    requirements: Mapped[Optional[str]] = mapped_column('requirements_flag', String(16))  # caom2:Observation.requirements.flag		
    instrument_name: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.instrument.name		
    instrument_keywords: Mapped[Optional[str]]  # caom2:Observation.instrument.keywords		
    environment_seeing: Mapped[Optional[float]] # caom2:Observation.environment.seeing		
    environment_humidity: Mapped[Optional[float]]  # caom2:Observation.environment.humidity		
    environment_elevation: Mapped[Optional[float]]  # caom2:Observation.environment.elevation		
    environment_tau: Mapped[Optional[float]]  # caom2:Observation.environment.tau		
    environment_wavelength_tau: Mapped[Optional[float]] = mapped_column('environment_wavelengthTau', Float)  # caom2:Observation.environment.wavelengthTau		
    environment_ambient_temp: Mapped[Optional[float]] = mapped_column('environment_ambientTemp', Float)  # caom2:Observation.environment.ambientTemp		
    environment_photometric: Mapped[Optional[bool]]  # caom2:Observation.environment.photometric		
    members: Mapped[Optional[str]]  # caom2:Observation.members		
    typeCode: Mapped[str]	= mapped_column(String(1))  # caom2:Observation.typeCode (C/S)
    metaProducer: Mapped[Optional[str]]  # caom2:Observation.metaProducer	uri	

    # Using validators to simplify ingest
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#simple-validators

    @validates("target_type")
    def validate_target_type(self, key, target_type):
        if target_type is not None:
            return target_type.value
    
    @validates("algorithm")
    def validate_algorithm(self, key, algorithm):
        if algorithm is not None:
            return algorithm.name

    def __repr__(self) -> str:
        return repr(f'Observation {self.observation_id}')
