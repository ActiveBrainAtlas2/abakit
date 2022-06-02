from abakit.lib.Controllers.AnnotationSessionController import AnnotationSessionController
from abakit.model.annotation_points import CellSources,MarkedCell
from abakit.lib.Controllers.Controller import Controller
class MarkedCellController(AnnotationSessionController):
    def __init__(self,*args,**kwargs):
        """initiates the controller class
        """        
        Controller.__init__(self,*args,**kwargs)

    def insert_marked_cells(self,coordinates,annotator_id,prep_id,cell_type_id, type:CellSources):
        session_id = self.add_marked_cell_session(prep_id=prep_id,annotator_id=annotator_id)
        for point in coordinates:
            cell = MarkedCell(x = point[0],y=point[1],z=point[2],source = type,FK_session_id=session_id,FK_cell_type_id=cell_type_id)
            self.add_row(cell)
