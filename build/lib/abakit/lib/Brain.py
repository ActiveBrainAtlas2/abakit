from abakit.lib.Controllers.SqlController import SqlController
from abakit.lib.FileLocationManager import FileLocationManager
from abakit.Plotter.Plotter import Plotter
import numpy as np


class Brain:
    """Basic class for the preprocessing pipeline, Cell Detection, contour processing and atlas creation
    """    

    def __init__(self, animal,*arg,**kwarg):
        """Initiates the brain object, starts the sqalchemy session, sets the location for the pipeline, readies the plotter 
        and loads the resolution of the brian

        Args:
            animal (string): Animal ID
        """        
        self.animal = animal
        self.sqlController = SqlController(self.animal)
        self.path = FileLocationManager(animal)
        self.plotter = Plotter()
        self.attribute_functions = dict(COM=self.load_com)
        to_um = self.get_resolution()
        self.pixel_to_um = np.array([to_um, to_um, 20])
        self.um_to_pixel = 1 / self.pixel_to_um
    
    def get_resolution(self):
        """get the scan resolution of the animal from the scan run table

        Returns:
            float: scan resolution
        """        
        return self.sqlController.scan_run.resolution
    
    def get_image_dimension(self):
        """get the dimension of the biggest image in the scan

        Returns:
            np array: np array of width and height
        """        
        width = self.sqlController.scan_run.width
        height = self.sqlController.scan_run.height
        return np.array([width, height])
    
    def check_attributes(self, attribute_list):
        """Checks if the class has certain attribute.
           If the attribute is not found, attempt to load/create the 
           attribute using a list of predefined functions

        Args:
            attribute_list (list of string): list of attribute names to check

        Raises:
            NotImplementedError: _description_
        """        
        assert(hasattr(self , 'attribute_functions'))
        for attribute in attribute_list:
            if not hasattr(self, attribute) or getattr(self, attribute) == {}:
                if attribute in self.attribute_functions:
                    self.attribute_functions[attribute]()
                else:
                    raise NotImplementedError
    
    def get_com_array(self):
        """Get the center of mass values for this brain as an array

        Returns:
            np array: COM of the brain 
        """        
        self.check_attributes(['COM'])
        return np.array(list(self.COM.values()))
        
    def load_com(self):
        """load the com attribute of this brain indexed by each region
        """        
        self.COM = self.sqlController.get_com_dict(self.animal)
    
    def get_shared_coms(self, com_dictionary1, com_dictionary2):
        """Get keys that are shared by two dictionaries

        Args:
            com_dictionary1 (dict): structure,coordinate pairing of structure com
            com_dictionary2 (dict): structure,coordinate pairing of structure com

        Returns:
            dictionary1,dictionary2: The two dictionaries, now only containing shared components
        """        
        shared_structures = set(com_dictionary1.keys()).intersection(set(com_dictionary2.keys()))
        values1 = [com_dictionary1[str] for str in shared_structures]
        values2 = [com_dictionary2[str] for str in shared_structures]
        com_dictionary1 = dict(zip(shared_structures, values1))
        com_dictionary2 = dict(zip(shared_structures, values2))
        return com_dictionary1, com_dictionary2
    
    def set_structure_from_attribute(self, possible_attributes_with_structure_list):
        """get the list of structure from a perticular attribute that is likely a dictionary
           with the structure abbreviations as the keys

        Args:
            possible_attributes_with_structure_list (list): list of attributes that could be used to get the list of structures
        """
        loaded_attributes = []
        for attributei in possible_attributes_with_structure_list:
            if hasattr(self, attributei) and getattr(self, attributei) != {}:
                if not hasattr(self, 'structures') or len(self.structures) == 0:
                    structures = self.get_structures_from_attribute(attributei)
                    self.structures = structures
                loaded_attributes.append(attributei)
        for attributei in loaded_attributes:
            assert(self.structures == self.get_structures_from_attribute(attributei))
        if loaded_attributes == []:
            self.load_com()
            self.structures = self.origins.keys()
    
    def get_structures_from_attribute(self, attribute):
        """return the structures that can be obtained from an attribute,
         the perticular attribute that is likely a dictionary

        Args:
            attribute (str): the name of attribute to get the list of structures from

        Returns:
            list: list of structures
        """        
        return list(getattr(self, attribute).keys())
    
    def convert_unit_of_com_dictionary(self, com_dictionary, conversion_factor):
        """convert the unit of every point in a com dictionary.
           The dictionary should be a set of 3d coordinates indexed by 
           structure name

        Args:
            com_dictionary (dict): COM dictionary to convert
            conversion_factor (np array): array of three converssion factors for x,y,z respectively
        """        
        for structure , com in com_dictionary.items():
            com_dictionary[structure] = np.array(com) * conversion_factor
