import numpy as np
import pytest
from util import get_test_volume_maker,get_correct_test_volume

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_volume_maker():
    maker = get_test_volume_maker()
    assert 'test' in maker.origins
    assert np.all(maker.origins['test'] == np.array([1,1,1]))
    assert 'test' in maker.volumes
    assert maker.volumes['test'].shape == (8,8,2)
    assert np.all(maker.volumes['test'][:3,:3,0]==True)
    assert np.sum(maker.volumes['test'][:,:,0])==9
    assert np.all(maker.volumes['test'][1:4,1:4,1]==True)
    assert np.sum(maker.volumes['test'][:,:,1])==9
    correct_volume = get_correct_test_volume()
    assert np.all(maker.volumes['test']==correct_volume)