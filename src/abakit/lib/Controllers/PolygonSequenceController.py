import numpy as np
from abakit.model.annotation_points import PolygonSequence
from abakit.model.annotation_session import AnnotationSession,AnnotationType
import json
import pandas as pd
from abakit.lib.Controllers.Controller import Controller

class PolygonSequenceController(Controller):
    def get_available_volumes(self):
        active_sessions = self.get_available_volumes_sessions()
        information = [[i.FK_prep_id,i.user.first_name,i.brain_region.abbreviation] for i in active_sessions]
        return information
    
    def get_volume(self,prep_id,annotator_id,structure_id):
        session = self.session.query(AnnotationSession)\
            .filter(AnnotationSession.FK_prep_id==prep_id)\
            .filter(AnnotationSession.FK_annotator_id==annotator_id)\
            .filter(AnnotationSession.FK_structure_id==structure_id)\
            .filter(AnnotationSession.active==1).first()   
        volume_points = self.session.query(PolygonSequence).filter(PolygonSequence.FK_session_id==session.id).all()
        volume = {}
        volume['coordinate']=[[i.x,i.y,i.z] for i in volume_points]
        volume['point_ordering']=[i.point_order for i in volume_points]
        volume['polygon_ordering']=[i.polygon_index for i in volume_points]
        volume = pd.DataFrame(volume)
        volume = volume.sort_values('polygon_ordering')
        return volume
    
    def get_available_volumes_sessions(self):
        active_sessions = self.session.query(AnnotationSession).\
            filter(AnnotationSession.annotation_type==AnnotationType.POLYGON_SEQUENCE)\
            .filter(AnnotationSession.active==1).all()
        return active_sessions