import SimpleITK as sitk
import numpy as np
import matplotlib as plt

class Transformation:
    def __init__():
        ...

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

    def find_transform_of_type(self,transform_type):
        return sitk.LandmarkBasedTransformInitializer(transform_type,list(self.fixed.flatten()),list(self.moving.flatten()))

    def visualize_transform(ax,point_set,N,nbrs,m='o',**linestyle):
        """ plot a 3d rendinring of a grid of points"""
        x=point_set[:,0]
        y=point_set[:,1]
        z=point_set[:,2]
        ax.scatter(x, y, z, marker=m)

        _coor=np.zeros([2,3])
        for i,j,color in nbrs:
            _coor[0,:]=point_set[i,:]
            _coor[1,:]=point_set[j,:]
            x=list(_coor[:,0])
            y=list(_coor[:,1])
            z=list(_coor[:,2])
            #print(i,j,a[i,:],a[j,:],color,x,y,z)
            ax.plot(x,y,z,color,**linestyle)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        xline=np.zeros([N])
        yline=np.zeros([N])
        zline=np.zeros([N])
        plt.show()