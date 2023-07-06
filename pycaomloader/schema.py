"""Database Schema defined by SQLAlchemy"""

# pylint: disable=trailing-whitespace, line-too-long, unused-argument, unused-import, missing-function-docstring, missing-class-docstring

from datetime import datetime
from uuid import UUID

from typing import Optional, List
from sqlalchemy import Integer, String, ForeignKey, Float, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, validates, relationship


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

    # Relationships
    planes: Mapped[List["CaomPlane"]] = relationship(back_populates="observation")

    # Using validators to simplify ingest
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#simple-validators

    @validates("target_type")
    def get_value(self, key, column):
        if column is not None:
            return column.value
    
    @validates("algorithm")
    def get_name(self, key, column):
        if column is not None:
            return column.name

    def __repr__(self) -> str:
        return repr(f'Observation {self.observation_id}')


class CaomPlane(CaomCommon, Base):
    """ CAOM Plane table """

    __tablename__ = "Plane"

    planeURI: Mapped[str] = mapped_column('planeURI', String)  # caom2:Plane.uri	uri	indexed
    publisherID: Mapped[Optional[str]]  # caom2:Plane.publisherID	uri	indexed
    obsID: Mapped[UUID]	= mapped_column(ForeignKey("Observation.obsID"))  # obsID	char(36)		true	foreign key			uuid	indexed
    id: Mapped[UUID] = mapped_column('planeID', primary_key=True)	# planeID	char(36)		true	unique plane identifier		caom2:Plane.id	uuid	indexed
    creatorID: Mapped[Optional[str]]  # caom2:Plane.creatorID	uri	indexed
    product_id: Mapped[str] = mapped_column('productID', String(256))  # caom2:Plane.productID		indexed
    meta_release: Mapped[Optional[datetime]] = mapped_column('metaRelease')   # caom2:Plane.metaRelease	timestamp	indexed
    meta_read_groups: Mapped[Optional[str]] = mapped_column('metaReadGroups')  # caom2:Plane.metaReadGroups		
    data_release: Mapped[Optional[datetime]] = mapped_column('dataRelease')  #  caom2:Plane.dataRelease	timestamp	indexed
    data_read_groups: Mapped[Optional[str]] = mapped_column('dataReadGroups')   # caom2:Plane.dataReadGroups		
    data_product_type: Mapped[Optional[str]] = mapped_column('dataProductType', String(128))  # caom2:Plane.dataProductType		
    calibration_level: Mapped[Optional[int]] = mapped_column('calibrationLevel')  # caom2:Plane.calibrationLevel		
    provenance_name: Mapped[Optional[str]] = mapped_column(String(128))  # caom2:Plane.provenance.name		
    provenance_version: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Plane.provenance.version		
    provenance_reference: Mapped[Optional[str]] = mapped_column(String(256))  # caom2:Plane.provenance.reference		
    provenance_producer: Mapped[Optional[str]] = mapped_column(String(128))  # caom2:Plane.provenance.producer		
    provenance_project: Mapped[Optional[str]] = mapped_column(String(256))  # caom2:Plane.provenance.project		
    provenance_run_id: Mapped[Optional[str]] = mapped_column('provenance_runID', String(64))  # caom2:Plane.provenance.runID		indexed
    provenance_last_executed: Mapped[Optional[datetime]] = mapped_column('provenance_lastExecuted')  # caom2:Plane.provenance.lastExecuted	timestamp	
    provenance_keywords: Mapped[Optional[str]]  #caom2:Plane.provenance.keywords		
    provenance_inputs: Mapped[Optional[str]]  # caom2:Plane.provenance.inputs	clob	
    metrics_source_number_density: Mapped[Optional[float]] = mapped_column('metrics_sourceNumberDensity')  # caom2:Plane.metrics.sourceNumberDensity		
    metrics_background: Mapped[Optional[float]]  # caom2:Plane.metrics.background		
    metrics_backgroundStddev: Mapped[Optional[float]]  # caom2:Plane.metrics.backgroundStddev		
    metrics_fluxDensityLimit: Mapped[Optional[float]]  # caom2:Plane.metrics.fluxDensityLimit		
    metrics_magLimit: Mapped[Optional[float]]   # caom2:Plane.metrics.magLimit		
    quality_flag: Mapped[Optional[str]] = mapped_column(String(16))  # caom2:Plane.quality.flag		
    position_bounds: Mapped[Optional[str]]  # caom2:Plane.position.bounds	caom2:shape	
    position_bounds_samples: Mapped[Optional[float]]  # caom2:Plane.position.bounds.samples	caom2:multipolygon	
    position_bounds_size: Mapped[Optional[float]]  # caom2:Plane.position.bounds.size		
    position_resolution: Mapped[Optional[float]]  # caom2:Plane.position.resolution		
    position_resolution_bounds: Mapped[Optional[float]] = mapped_column('position_resolutionBounds')  # caom2:Plane.position.resolutionBounds	interval	
    position_sampleSize: Mapped[Optional[float]]  # caom2:Plane.position.sampleSize		
    position_dimension_naxis1: Mapped[Optional[int]]  # caom2:Plane.position.dimension.naxis1		
    position_dimension_naxis2: Mapped[Optional[int]]  # caom2:Plane.position.dimension.naxis2		
    position_time_dependent: Mapped[Optional[bool]] = mapped_column('position_timeDependent')  # caom2:Plane.position.timeDependent		
    energy_bounds: Mapped[Optional[float]]  # caom2:Plane.energy.bounds	interval	indexed
    energy_bounds_samples: Mapped[Optional[float]]  # caom2:Plane.energy.bounds.samples	caom2:multiinterval	
    energy_bounds_lower: Mapped[Optional[float]]  # caom2:Plane.energy.bounds.lower		indexed
    energy_bounds_upper: Mapped[Optional[float]]  # caom2:Plane.energy.bounds.upper		indexed
    energy_bounds_width: Mapped[Optional[float]]  # caom2:Plane.energy.bounds.width		
    energy_dimension: Mapped[Optional[float]]  # caom2:Plane.energy.dimension		
    energy_resolving_power: Mapped[Optional[float]] = mapped_column('energy_resolvingPower')  # caom2:Plane.energy.resolvingPower		
    energy_resolving_power_bounds: Mapped[Optional[float]] = mapped_column('energy_resolvingPowerBounds')  # caom2:Plane.energy.resolvingPowerBounds	interval	
    energy_sample_size: Mapped[Optional[float]] = mapped_column('energy_sampleSize')  # caom2:Plane.energy.sampleSize		
    energy_em_band: Mapped[Optional[str]] = mapped_column('energy_emBand', String(32))                 # caom2:Plane.energy.emBand		
    energy_energy_bands: Mapped[Optional[str]] = mapped_column('energy_energyBands', String(32))            # caom2:Plane.energy.energyBands		
    energy_bandpass_name: Mapped[Optional[str]] = mapped_column('energy_bandpassName', String(32))           # caom2:Plane.energy.bandpassName		
    energy_transition_species: Mapped[Optional[str]] = mapped_column(String(32))     # caom2:Plane.energy.transition.species		
    energy_transition_transition: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Plane.energy.transition.transition		
    energy_freq_width: Mapped[Optional[float]] = mapped_column('energy_freqWidth')      # caom2:Plane.energy.freqWidth		
    energy_freq_sample_size: Mapped[Optional[float]] = mapped_column('energy_freqSampleSize') # caom2:Plane.energy.freqSampleSize		
    energy_restwav: Mapped[Optional[float]]        # caom2:Plane.energy.restwav		indexed
    time_bounds: Mapped[Optional[float]]           # caom2:Plane.time.bounds	interval	indexed
    time_bounds_lower: Mapped[Optional[float]]     # caom2:Plane.time.bounds.lower		indexed
    time_bounds_samples: Mapped[Optional[float]]   # caom2:Plane.time.bounds.samples	caom2:multiinterval	
    time_bounds_upper: Mapped[Optional[float]]     # caom2:Plane.time.bounds.upper		indexed
    time_bounds_width: Mapped[Optional[float]]     # indexed
    time_dimension: Mapped[Optional[int]]          # caom2:Plane.time.dimension		
    time_resolution: Mapped[Optional[float]]       # caom2:Plane.time.resolution		
    time_resolutionBounds: Mapped[Optional[float]] # caom2:Plane.time.resolutionBounds	interval	
    time_sampleSize: Mapped[Optional[float]]       # caom2:Plane.time.sampleSize		
    time_exposure: Mapped[Optional[float]]         # caom2:Plane.time.exposure		
    polarization_states: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Plane.polarization.states		
    polarization_dimension: Mapped[Optional[int]]  # caom2:Plane.polarization.dimension		
    custom_ctype: Mapped[Optional[str]] = mapped_column(String(32))  # caom2:Plane.custom.ctype		
    custom_bounds: Mapped[Optional[float]]  # caom2:Plane.custom.bounds	interval	
    custom_bounds_samples: Mapped[Optional[float]]  # caom2:Plane.custom.bounds.samples	caom2:multiinterval	
    custom_bounds_lower: Mapped[Optional[float]]  # caom2:Plane.custom.bounds.lower		
    custom_bounds_upper: Mapped[Optional[float]]  # caom2:Plane.custom.bounds.upper		
    custom_bounds_width: Mapped[Optional[float]]  # caom2:Plane.custom.bounds.width		
    custom_dimension: Mapped[Optional[int]]  # caom2:Plane.custom.dimension		
    metaProducer: Mapped[Optional[str]]	 # caom2:Plane.metaProducer	uri	

    # Relationships
    observation = relationship("CaomObservation", back_populates="planes")

    @validates("calibration_level", "data_product_type")
    def get_value(self, key, column):
        if column is not None:
            return column.value

    def __repr__(self) -> str:
        return repr(f'Plane {self.product_id}')
