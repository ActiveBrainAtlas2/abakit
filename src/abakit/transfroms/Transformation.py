import SimpleITK as sitk
import numpy as np
import matplotlib as plt
from scipy.ndimage.interpolation import affine_transform

class Transformation:
    def set_fixed_and_moving_points(self,fixed,moving):
        self.fixed = fixed
        self.moving = moving

    def transform_points(transform,points):
        """Transform a set of points according to a given transformation
        transform: and instance of SimpleITK.SimpleITK.Transform
        points: a numpy array of shape (number of points) X (number of dimensions)
        return moved: a numpy array of the same shape as points"""
        npoints,_=points.shape
        transformed_points=np.zeros(points.shape)
        for pointi in range(npoints):
            transformed_points[pointi]=transform.TransformPoint(points[pointi,:])
        return transformed_points
    
    def plot_difference_between_pointsets(point_set1,point_set2):
        point_set_difference=(point_set1-point_set2)
        plt.hist(point_set_difference.flatten(),bins=100)
        plt.grid()

    def find_affine_transform(self):
        self.affine_transform = self.find_transform_of_type(sitk.AffineTransform(3))
        self.inverse_affine_transform = self.affine_transform.GetInverse()

    def find_rigid_transform(self):
        self.rigid_transform = self.find_transform_of_type(sitk.VersorRigid3DTransform())
        self.inverse_rigid_transform = self.rigid_transform.GetInverse()

    def get_affine_transform(self):
        if not hasattr(self,'affine_transform'):
            self.find_affine_transform()
        return self.affine_transform
    
    def get_rigid_transform(self):
        if not hasattr(self,'rigid_transform'):
            self.find_rigid_transform()
        return self.rigid_transform

    def find_transform_of_type(self,transform_type):
        return sitk.LandmarkBasedTransformInitializer(transform_type,list(self.fixed.flatten()),list(self.moving.flatten()))