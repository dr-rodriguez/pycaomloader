# Database Schema defined by SQLAlchemy

import sqlalchemy as sa

from datetime import datetime
from uuid import UUID

from typing import Optional
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import MetaData


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
    # Common columns for all CAOM Tables

    lastModified: Mapped[Optional[datetime]]  # caom2:Observation.lastModified	timestamp	
    maxLastModified: Mapped[Optional[datetime]]  # caom2:Observation.maxLastModified	timestamp	
    metaChecksum: Mapped[Optional[str]]  # caom2:Observation.metaChecksum	uri	
    accMetaChecksum: Mapped[Optional[str]]  # caom2:Observation.accMetaChecksum	uri	


class CaomObservation(CaomCommon, Base):
    __tablename__ = "Observation"

    observationURI: Mapped[str]  # caom2:Observation.uri	uri	indexed
    obsID: Mapped[UUID] = mapped_column(primary_key=True)	# caom2:Observation.id	uuid	indexed
    collection: Mapped[str] = mapped_column(String(32))  # caom2:Observation.collection		indexed
    observationID: Mapped[str] = mapped_column(String(128))  # caom2:Observation.observationID		indexed
    algorithm_name: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.algorithm.name
    type: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.type		
    intent: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.intent		
    sequenceNumber: Mapped[Optional[int]]  # caom2:Observation.sequenceNumber		
    metaRelease: Mapped[Optional[datetime]]  # caom2:Observation.metaRelease	timestamp	
    metaReadGroups: Mapped[Optional[str]]  # caom2:Observation.metaReadGroups		
    proposal_id: Mapped[str] = mapped_column(String(128))  # caom2:Observation.proposal.id		indexed
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
    telescope_geoLocationX: Mapped[Optional[float]]  # caom2:Observation.telescope.geoLocationX		
    telescope_geoLocationY: Mapped[Optional[float]]  # caom2:Observation.telescope.geoLocationY		
    telescope_geoLocationZ: Mapped[Optional[float]]  # caom2:Observation.telescope.geoLocationZ		
    telescope_keywords: Mapped[Optional[str]]  # caom2:Observation.telescope.keywords		
    requirements_flag: Mapped[Optional[str]] = mapped_column(String(16))  # caom2:Observation.requirements.flag		
    instrument_name: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Observation.instrument.name		
    instrument_keywords: Mapped[Optional[str]]  # caom2:Observation.instrument.keywords		
    environment_seeing: Mapped[Optional[float]] # caom2:Observation.environment.seeing		
    environment_humidity: Mapped[Optional[float]]  # caom2:Observation.environment.humidity		
    environment_elevation: Mapped[Optional[float]]  # caom2:Observation.environment.elevation		
    environment_tau: Mapped[Optional[float]]  # caom2:Observation.environment.tau		
    environment_wavelengthTau: Mapped[Optional[float]]  # caom2:Observation.environment.wavelengthTau		
    environment_ambientTemp: Mapped[Optional[float]]  # caom2:Observation.environment.ambientTemp		
    environment_photometric: Mapped[Optional[bool]]  # caom2:Observation.environment.photometric		
    members: Mapped[Optional[str]]  # caom2:Observation.members		
    typeCode: Mapped[str]	= mapped_column(String(1))  # caom2:Observation.typeCode (C/S)
    metaProducer: Mapped[Optional[str]]  # caom2:Observation.metaProducer	uri	

