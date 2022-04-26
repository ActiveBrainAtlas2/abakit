from abakit.atlas.NgSegmentMaker import NgConverter
import numpy as np
import os
import shutil
import pytest
from util import get_test_volume_maker

def read_file(path):
    text_file = open(path, "r")
    data = text_file.read()
    text_file.close()
    return data

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_contour_to_segments():
    test_folder = os.path.dirname(__file__)
    output_dir = test_folder+'/ngsegment_test'
    vmaker = get_test_volume_maker()
    structure = 'test'
    maker = NgConverter(volume = vmaker.volumes[structure].astype(np.uint8),scales = [1,1,1],offset=list(vmaker.origins[structure]))
    segment_properties  = [('1','test')]
    maker.create_neuroglancer_files(output_dir,segment_properties)
    vmaker.get_segment_properties()[0]
    assert os.path.exists(output_dir)
    assert os.listdir(output_dir) == ['info', '1_1_1', 'names', 'provenance', 'mesh_mip_0_err_40']
    assert os.path.getsize(output_dir) >50
    info_file = read_file(output_dir+'/info')
    correct_info_file = read_file(test_folder+'/example_info_file')
    assert info_file == correct_info_file
    shutil.rmtree(output_dir)