from abakit.lib.Controllers.Controller import Controller


class BrainShapeController(Controller):
    """Methods to access data in 'brain_shape' table
    -DB defined in settings.py
    -Table schema defined in model/brain_shape.py (BrainShape model)

    :param Controller: Extends Controller (SQLAchemy)
    """

    
    def insert_shapes(self):
        """Stores dimensions, offsets and np BLOB data for transformations (3D mask in stack or atlas coordinates)
        """        
        pass
    

    def get_shapes(self, ids) -> dict:
        """Query table for actual transformations

        :param ids: list of id to be retrieved from table (id is index on brain_shape table)
        :type ids: list of int [from brain_shape table]

        :return: Dictionary of transformations
        """        
        pass
    

    def get_available_shapes(self, prep_id: str, structure: int = None) -> dict:
        """Capture available transformations
        
        :param prep_id: prep_id of 3D mask to be transformed
        :param structure: brain structure of 3D mask to be transformed
        :type structure: int, optional (index 'id' from structure table)

        :return: Dictionary of available transformations, given brain and optional structure
        """
        pass