from abakit.model.annotation_points import StructureCOM,COMSources
from abakit.lib.Controllers.Controller import Controller
from abakit.lib.Controllers.AnnotationSessionController import AnnotationSessionController

class StructureComController(AnnotationSessionController):
    '''The class that queries and addes entry to the StructureCom table'''
    
    def __init__(self,*args,**kwargs):
        """initiates the controller class
        """        
        Controller.__init__(self,*args,**kwargs)

    def get_COM(self,prep_id,annotator_id):
        """returns the Center Of Mass of structures for a Animal ID and annotator combination

        Args:
            prep_id (str): Animal ID
            annotator_id (int): Annotator Id

        Returns:
            dict: dictionary of x,y,z coordinates indexed by structure name
        """    
        coms = self.session.query(StructureCOM)\
            .filter(StructureCOM.source.FK_prep_id==prep_id)\
            .filter(StructureCOM.source.FK_annotator_id==annotator_id)\
            .filter(StructureCOM.source.active==1).all()   
        coordinate = [[i.x,i.y,i.z] for i in coms]
        structure = [i.source.brain_region.abbreviation for i in coms]
        return dict(zip(structure,coordinate))
    
    def insert_com(self,coordinates,annotator_id,prep_id,structure_id, type:COMSources):
        session_id = self.add_structure_com_session(prep_id=prep_id,annotator_id=annotator_id,structure_id=structure_id)
        for point in coordinates:
            com = StructureCOM(x = point[0],y=point[1],z=point[2],source = type,FK_session_id=session_id)
            self.add_row(com)