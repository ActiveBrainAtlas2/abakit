from abakit.lib.Controllers.AnnotationSessionController import AnnotationSessionController
from abakit.model.annotation_points import CellSources,MarkedCell
class MarkedCellController(AnnotationSessionController):

    def insert_marked_cells(self,coordinates,annotator_id,prep_id,cell_type_id, type:CellSources):
        session_id = self.add_marked_cell_session(prep_id=prep_id,annotator_id=annotator_id)
        for point in coordinates:
            cell = MarkedCell(x = point[0],y=point[1],z=point[2],source = type,FK_session_id=session_id,FK_cell_type_id=cell_type_id)
            self.add_row(cell)
