import numpy as np
from abakit.model.annotation_points import PolygonSequence
from abakit.model.annotation_session import AnnotationSession
import json
import pandas as pd
from abakit.lib.Controllers.Controller import Controller

class PolygonSequenceController(Controller):
    def get_available_volumes(self):
        active_sessions = self.session.query(PolygonSequence).distinct(PolygonSequence.FK_session_id).all()
        information = [[i.session.FK_prep_id,i.user,i.brain_region.abbreviation] for i in active_sessions]
        return np.unique(information)
    
    def get_volume(self,prep_id,user_id,structure_id):
        active_sessions = self.session.query(PolygonSequence).distinct(PolygonSequence.FK_session_id).all()