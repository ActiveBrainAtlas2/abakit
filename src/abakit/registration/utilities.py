from .algorithm import umeyama
import numpy as np
import copy
def get_rigid_transformation_from_dicts(com_dict1,com_dict2):
    common_landmarks = (set(com_dict1.keys()).intersection(set(com_dict2.keys())))
    com_dict1 = np.array([com_dict1[landmark] for landmark in common_landmarks])
    com_dict2 = np.array([com_dict2[landmark] for landmark in common_landmarks])
    rigid_transformation = umeyama(com_dict1.T,com_dict2.T)
    return rigid_transformation

def get_and_apply_transform(moving_com,still_com):
    affine_transform = umeyama(moving_com.T,still_com.T)
    transformed_coms = apply_rigid_transform_to_points(moving_com,affine_transform)
    return transformed_coms,affine_transform

def apply_rigid_transformation_to_com(com,rigid_transformation):
    rotation,translation = rigid_transformation
    return rotation@np.array(com).reshape(3)+ translation.reshape(3)

def apply_rigid_transform_to_points(coms,rigid_transform):
    transformed_com_list = []
    for com in coms:
        transformed_com = apply_rigid_transformation_to_com(com,rigid_transform)
        transformed_com_list.append(transformed_com)
    return np.array(transformed_com_list)

def apply_rigid_transformation_to_com_dict(com_dict,rigid_transformation):
    for landmark,com in com_dict.items():
        com_dict[landmark] = apply_rigid_transformation_to_com(com,rigid_transformation)
    return com_dict

def apply_rigid_transformation_to_com_dict_list(com_dict_list,rigid_transformation):
    com_dict_list_copy = copy.deepcopy(com_dict_list)
    rigid_transformed_com_dicts = [apply_rigid_transformation_to_com_dict(com_dict,rigid_transformation) for com_dict in com_dict_list_copy]
    return rigid_transformed_com_dicts