from abakit.lib.Controllers.Controller import Controller
from abakit.model.annotation_session import AnnotationSession,AnnotationType
from abakit.model.annotation_points import CellSources,COMSources,PolygonSequence
class AnnotationSessionController(Controller):
    def add_marked_cell_session(self,prep_id,annotator_id):
        session = AnnotationSession(FK_prep_id = prep_id,FK_annotator_id = annotator_id,FK_structure_id=52,annotation_type=AnnotationType.MARKED_CELL,FK_parent=0)
        self.add_row(session)
        return session.id

    def add_structure_com_session(self,prep_id,annotator_id,structure_id):
        session = AnnotationSession(FK_prep_id = prep_id,FK_annotator_id = annotator_id,FK_structure_id=structure_id,annotation_type=AnnotationType.STRUCTURE_COM,FK_parent=0)
        self.add_row(session)
        return session.id

    def add_polygon_sequence_session(self,prep_id,annotator_id,structure_id):
        session = AnnotationSession(FK_prep_id = prep_id,FK_annotator_id = annotator_id,FK_structure_id=structure_id,annotation_type=AnnotationType.POLYGON_SEQUENCE,FK_parent=0)
        self.add_row(session)
        return session.id

    def delete_annotation_session(self,search_dictionary):
        self.delete_row(search_dictionary,AnnotationSession)