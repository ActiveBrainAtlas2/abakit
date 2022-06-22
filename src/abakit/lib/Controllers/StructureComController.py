import numpy as np
from abakit.model.annotation_points import StructureCOM
import json
import pandas as pd
from abakit.lib.Controllers.Controller import Controller

class StructureComController(Controller):
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
    