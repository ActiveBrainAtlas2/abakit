
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey,Enum
from sqlalchemy.sql.sqltypes import Float
from abakit.model.atlas_model import Base
from abakit.model.brain_region import BrainRegion
import enum

class AnnotationPoint(Base):
    __tablename__ = 'annotations_points'
    id =  Column(Integer, primary_key=True, nullable=False)
    prep_id = Column(String, nullable=False)
    FK_input_id = Column(Integer)
    FK_owner_id = Column(Integer)
    FK_structure_id = Column(Integer, ForeignKey('structure.id'), nullable=True)
    label = Column(String, nullable=False)
    polygon_id = Column(String, nullable=True)
    volume_id = Column(String, nullable=True)
    ordering = Column(Integer, nullable=False, default=0)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    ordering = Column(Integer)
    
    brain_region = relationship('BrainRegion', lazy=True)
    active = Column(Integer)


class CellSources(enum.Enum):
    MACHINE_SURE = 'MACHINE-SURE'
    MACHINE_UNSURE = 'MACHINE-UNSURE'
    HUMAN_POSITIVE = 'HUMAN-POSITIVE'
    HUMAN_NEGATIVE = 'HUMAN-NEGATIVE'

class MarkedCell(Base):
    __tablename__ = 'marked_cells'
    id =  Column(Integer, primary_key=True, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    source = Column(Enum(CellSources))    
    FK_session_id = Column(Integer, ForeignKey('annotation_session.id'), nullable=True)

class COMSources(enum.Enum):
    MANUAL = 'MANUAL'
    COMPUTER = 'COMPUTER'

class StructureCOM(Base):
    __tablename__ = 'structure_com'
    id =  Column(Integer, primary_key=True, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    source = Column(Enum(COMSources))    
    FK_session_id = Column(Integer, ForeignKey('annotation_session.id'), nullable=True)

class PolygonSources(enum.Enum):
    NA = 'NA'

class PolygonSequence(Base):
    __tablename__ = 'polygon_sequences'
    id =  Column(Integer, primary_key=True, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    source = Column(Enum(PolygonSources))    
    FK_session_id = Column(Integer, ForeignKey('annotation_session.id'), nullable=True)
    polygon_index = Column(Integer)
    point_order = Column(Integer)