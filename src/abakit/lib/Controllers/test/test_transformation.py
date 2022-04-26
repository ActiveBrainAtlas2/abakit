from abakit.lib.Controllers.TransformationController import TransformationController
import numpy as np
def test_transformation():
    controller = TransformationController()
    transform = controller.get_transformation(source = 'DK39',destination = 'Atlas', transformation_type = 'Rigid')
    points = np.random.rand(30).reshape(10,3)
    transformed_points = transform.forward_transform_points(points)
    recovered_points = transform.inverse_transform_points(transformed_points)
    assert np.all(np.isclose(points,recovered_points))