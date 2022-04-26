import SimpleITK as sitk
from SimpleITK.SimpleITK import Transform
import numpy as np

class Transformation:

    def __init__(self,fixed_and_regular_parameters,type):
        self.fixed_and_regular_parameters = fixed_and_regular_parameters
        self.type = type
    
    def inverse_transform_points(self,points):
        self.create_inverse_transform()
        transformed_points = self.transform_points(points,self.inverse_transform.TransformPoint)
        return transformed_points
    
    def forward_transform_points(self,points):
        self.create_transform()
        transformed_points = self.transform_points(points,self.transform.TransformPoint)
        return transformed_points

    def transform_points(self,points,tranform_function):
        """Transform a set of points according to a given transformation
        transform: and instance of SimpleITK.SimpleITK.Transform
        points: a numpy array of shape (number of points) X (number of dimensions)
        return moved: a numpy array of the same shape as points"""
        points = np.array(points)
        self.create_transform()
        transpose = False
        if points.shape[1] != 3 and points.shape[0] == 3:
            points = points.T
            transpose = True
        npoints,_=points.shape
        transformed_points=np.zeros(points.shape)
        for pointi in range(npoints):
            transformed_points[pointi]=tranform_function(points[pointi,:].tolist())
        if transpose:
            transformed_points = transformed_points.T
        return transformed_points
    
    def create_inverse_transform(self):
        self.create_transform()
        if not hasattr(self,'inverse_transform'):
            self.inverse_transform = self.transform.GetInverse()
        return self.inverse_transform
    
    def create_transform(self):
        if not hasattr(self,'transform'):
            self.transform = self.type()
            self.transform.SetFixedParameters(self.fixed_and_regular_parameters[0])
            self.transform.SetParameters(self.fixed_and_regular_parameters[1])