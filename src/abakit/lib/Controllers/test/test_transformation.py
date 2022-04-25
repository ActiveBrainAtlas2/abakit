from abakit.Controllers.TransformationController import TransformationController

def test_transformation():
    controller = TransformationController()
    transform = controller.get_row(dict(source = 'DK39',destination = 'Atlas', transformation_type = 1))

if __name__ == '__main__':
    test_transformation()