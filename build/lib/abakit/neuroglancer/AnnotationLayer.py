import numpy as np
class AnnotationLayer:
    def __init__(self,annotation_layer):
        assert annotation_layer['type'] == 'annotation'
        self.annotations = annotation_layer['annotations']
        self.name = annotation_layer['name']
        self.tool = annotation_layer['tool']
        self.source = annotation_layer['source']
        self.type = 'annotation'
        self.parse_annotations()
    
    def parse_annotations(self):
        annotations = []
        for annotationi in self.annotations:
            if annotationi['type']=='polygon':
                annotations.append(self.parse_polygon(annotationi))
            elif annotationi['type']=='point':
                annotations.append(self.parse_point(annotationi))
            elif annotationi['type']=='line':
                annotations.append(self.parse_line(annotationi))
        self.annotations = np.array(annotations)

        for annotationi in self.annotations:
            if annotationi.type == 'polygon':
                for childid in annotationi.child_ids:
                    annotationi.childs.append(self.get_annotation_with_id(childid))
                    self.delete_annotation_with_id(childid)

    
    def parse_point(self,point_json):
        return Point(point_json['point'],point_json['id'])
    
    def parse_line(self,line_json):
        line = Line(line_json['pointA'],line_json['pointB'],line_json['id'])
        if 'parentAnnotationId' in line_json:
            line.parent_id = line_json['parentAnnotationId']
        return line

    def parse_polygon(self,polygon):
        return Polygon(polygon['id'],polygon['childAnnotationIds'],polygon['source'])
    
    def search_annotation_with_id(self,id):
        search_result = [annotationi.id == id for annotationi in self.annotations]
        if sum(search_result)==0:
            print('annotation not found')
        elif sum(search_result)>1:
            print('more than one result found')
        return search_result
    
    def get_annotation_with_id(self,id):
        search_result = self.search_annotation_with_id(id)
        return self.annotations[search_result]
    
    def delete_annotation_with_id(self,id):
        search_result = self.search_annotation_with_id(id)
        self.annotations = self.annotations[np.logical_not(search_result)]
    
    def to_json(self):
        point_json = {}
        ...

class Point:
    def __init__(self,coord,id):
        self.coord = coord
        self.id = id
        self.type = 'point'
    
    def to_json(self):
        point_json = {}
        ...

class Line:
    def __init__(self,coord_start,coord_end,id):
        self.coord_start = coord_start
        self.coord_end = coord_end
        self.id = id
        self.type = 'line'


    def to_json(self):
        ...

class Polygon:
    def __init__(self,id,child_ids,source):
        self.source = source
        self.id = id
        self.child_ids = child_ids
        self.childs=[]
        self.type = 'polygon'
    
    def to_json(self):
        ...