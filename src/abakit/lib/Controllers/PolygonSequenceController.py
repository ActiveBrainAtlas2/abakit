import numpy as np
from abakit.model.annotation_points import PolygonSequence
from abakit.model.annotation_session import AnnotationSession
import json
import pandas as pd
from abakit.lib.Controllers.Controller import Controller

class PolygonSequenceController(Controller):
    def get_available_polygons(self):
        active_sessions = self.session.query(PolygonSequence).distinct(PolygonSequence.FK_session_id).all()