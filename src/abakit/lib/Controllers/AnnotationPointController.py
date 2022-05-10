import numpy as np
from abakit.model.annotation_points import AnnotationPoint
import json
import pandas as pd
from abakit.lib.Controllers.Controller import Controller

class AnnotationPointController(Controller):
    """This class is about to be depricated as the annotation points table are to be split into the PolygonSequence,
       StructureCom and MarkedCells table
    """
    def __init__(self):
        super().__init__()

    def get_annotation_points_orm(self,search_dictionary):
        """The main function for querying the annoataion points table

        Args:
            search_dictionary (dict): column name and value pair for the search

        Returns:
            list: list of sqlalchemy ORM objects
        """        
        return self.query_table(search_dictionary,AnnotationPoint)
    
    def add_annotation_points(self, abbreviation, animal, layer, x, y, section, 
                       person_id, input_type_id):
        """adding a row to annotation points table

        Args:
            abbreviation (string): structure name short hand
            animal (string): animal name
            layer (string): layer name
            x (float): x coordinate
            y (float): y coordinate
            section (int): z section number
            person_id (int): id of annotator 
            input_type_id (int): id of input type
        """
        structure_id = self.structure_abbreviation_to_id(abbreviation)
        coordinates = (x,y,section)
        self.add_annotation_points(animal,person_id,input_type_id,coordinates,structure_id,layer)

    def get_annotation_points(self, prep_id, input_type_id=1, person_id=2,active = True,layer = 'COM'):
        """function to obtain coordinates of annotation points

        Args:
            prep_id (str): Animal ID
            input_type_id (int, optional): int for input type. Defaults to 1.
            person_id (int, optional): annotation id. Defaults to 2.
            active (bool, optional): search of active or inactive annotations. Defaults to True.
            layer (str, optional): layer name. Defaults to 'COM'.

        Returns:
            _type_: _description_
        """        
        search_dictionary=dict( prep_id = prep_id,
                                input_type_id = input_type_id,
                                person_id = person_id,
                                layer = layer,
                                active=0)
        rows = self.get_annotation_points_orm(search_dictionary)
        search_result = {}
        for row in rows:
            structure = row.structure.abbreviation
            search_result[structure] = [row.x, row.y, row.section]
        return search_result


    def add_annotation_points(self,animal,person_id,input_type_id,coordinates,structure_id,layer):
        """adding a row to the annotation points table

        Args:
            animal (str): Animal ID
            person_id (int): Annotator ID
            input_type_id (int): Input Type ID
            coordinates (list): list of x,y,z coordinates
            structure_id (int): Structure ID
            layer (str): layer name
        """        
        x,y,z = coordinates
        data = AnnotationPoint(prep_id = animal, person_id = person_id, input_type_id = input_type_id, x=x, y=y, \
            section=z,structure_id=structure_id,layer=layer)
        self.add_row(data)
    
    def add_com(self, prep_id, abbreviation, coordinates, person_id=2 , input_type_id = 1):
        """Adding a Com Entry

        Args:
            prep_id (str): Animal ID
            abbreviation (str): structure abbreviation
            coordinates (list): list of x,y,z coordinates
            person_id (int, optional): Annotator ID. Defaults to 2.
            input_type_id (int, optional): Input Type ID. Defaults to 1.
        """        
        structure_id = self.structure_abbreviation_to_id(abbreviation)
        if self.layer_data_row_exists(animal=prep_id,person_id = person_id,input_type_id = input_type_id,\
            structure_id = structure_id,layer = 'COM'):
            self.delete_layer_data_row(animal=prep_id,person_id = person_id,input_type_id = input_type_id,\
                structure_id = structure_id,layer = 'COM')
        self.add_annotation_points(animal = prep_id,person_id = person_id,input_type_id = input_type_id,\
            coordinates = coordinates,structure_id = structure_id,layer = 'COM')
    
    def layer_data_row_exists(self,animal, person_id, input_type_id, structure_id, layer):
        row_exists = bool(self.session.query(AnnotationPoint).filter(
            AnnotationPoint.prep_id == animal, 
            AnnotationPoint.person_id == person_id, 
            AnnotationPoint.input_type_id == input_type_id, 
            AnnotationPoint.structure_id == structure_id,
            AnnotationPoint.layer == layer).first())
        return row_exists
 
    def delete_layer_data_row(self,animal,person_id,input_type_id,structure_id,layer):
        self.session.query(AnnotationPoint)\
            .filter(AnnotationPoint.active.is_(True))\
            .filter(AnnotationPoint.prep_id == animal)\
            .filter(AnnotationPoint.input_type_id == input_type_id)\
            .filter(AnnotationPoint.person_id == person_id)\
            .filter(AnnotationPoint.structure_id == structure_id)\
            .filter(AnnotationPoint.layer == layer).delete()
        self.session.commit()
    
    def get_com_dict(self, prep_id, input_type_id=1, person_id=2,active = True):
        return self.get_annotation_points( prep_id = prep_id, input_type_id=input_type_id,\
             person_id=person_id,active = active,layer = 'COM')

    def get_atlas_centers(self):
        PERSON_ID_LAUREN = 16
        INPUT_TYPE_MANUAL = 1
        return self.get_com_dict('Atlas',INPUT_TYPE_MANUAL,PERSON_ID_LAUREN)
    
    def get_point_dataframe(self, id):
        """
        :param id: primary key from the url. Look at:
         https://activebrainatlas.ucsd.edu/activebrainatlas/admin/neuroglancer/points/164/change/
         for example use 164 for the primary key
         to get the ID
        :return: a pandas dataframe
        """

        try:
            urlModel = self.session.query(
                UrlModel).filter(UrlModel.id == id).one()
        except NoResultFound as nrf:
            print('Bad ID for {} error: {}'.format(id, nrf))
            return

        result = None
        dfs = []
        if urlModel.url is not None:
            json_txt = json.loads(urlModel.url)
            layers = json_txt['layers']
            for l in layers:
                if 'annotations' in l:
                    name = l['name']
                    annotation = l['annotations']
                    d = [row['point'] for row in annotation]
                    df = pd.DataFrame(d, columns=['X', 'Y', 'Section'])
                    df['X'] = df['X'].astype(int)
                    df['Y'] = df['Y'].astype(int)
                    df['Section'] = df['Section'].astype(int)
                    df['Layer'] = name
                    df = df[['Layer', 'X', 'Y', 'Section']]
                    dfs.append(df)
            if len(dfs) == 0:
                result = None
            elif len(dfs) == 1:
                result = dfs[0]
            else:
                result = pd.concat(dfs)

        return result
    
    def get_annotated_animals(self):
        results = self.session.query(AnnotationPoint)\
            .filter(AnnotationPoint.active.is_(True))\
            .filter(AnnotationPoint.input_type_id == 1)\
            .filter(AnnotationPoint.person_id == 2)\
            .filter(AnnotationPoint.layer == 'COM').all()
        return np.unique([ri.prep_id for ri in results])