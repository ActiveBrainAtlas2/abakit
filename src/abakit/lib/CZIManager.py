import os
from PIL import Image
from aicspylibczi import CziFile
from tifffile import imsave
from abakit.lib.utilities_mask import equalized
class CZIManager:
    def __init__(self,czi_file):
        self.czi_file = czi_file
        self.file = CziFile(czi_file)

    def get_nscene(self):
        if not hasattr(self,'nscene'):
            self.nscene = int(self.file.meta[0][4][3][7].text)
        return self.nscene
    
    def get_nchannel(self):
        if not hasattr(self,'nchannel'):
            self.nchannel = int(self.file.meta[0][4][3][1].text)
        return self.nchannel
    
    def get_scene_dimension(self,scene_index):
        scene = self.file.get_scene_bounding_box(scene_index)
        return scene.x,scene.y,scene.w,scene.h
    
    def get_scene(self,scene_index,channel,scale=1):
        region = self.get_scene_dimension(scene_index)
        return self.file.read_mosaic(region=region,scale_factor=scale,C=channel)[0]

def extract_tiff_from_czi(czi_file,file_name,channel=1,scale=1):
    czi = CZIManager(czi_file)
    nscenes = czi.get_nscene()
    for scenei in range(nscenes):
        data = czi.get_scene(scale=scale,scene_index=scenei,channel = channel)
        imsave(file_name,data)

def extract_png_from_czi(czi_file,file_name,channel=1,scale=1,normalize = True):
    czi = CZIManager(czi_file)
    nscenes = czi.get_nscene()
    for scenei in range(nscenes):
        data = czi.get_scene(scale=scale,scene_index=scenei,channel = channel)
        if normalize:
            data = equalized(data)
        im = Image.fromarray(data)
        im.save(file_name)
