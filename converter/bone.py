import numpy as np
import re
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import quaternion

class Bone:
    Pattern = re.compile(r'bone \d+ {[\s\S]*?}')
    NamePattern = re.compile(r'name "(\w+)"')
    BindPosPattern = re.compile(r'bindpos ((?:-?\d+\.?\d* ?){3})')
    BindMatPattern = re.compile(r'bindmat ((?:-?\d+\.?\d* ?){9})')
    ParentPattern = re.compile(r'parent "(\w+)"')

    def __init__(self, idx, bonebuf):
        self.name = Bone.NamePattern.search(bonebuf).group(1)
        self.bindpos = Bone.BindPosPattern.search(bonebuf).group(1)
        self.bindmat = Bone.BindMatPattern.search(bonebuf).group(1)
        maybeParent = Bone.ParentPattern.search(bonebuf)
        self.parent = maybeParent.group(1) if maybeParent else None
        self.idx = idx

    def convert(self, boneTable):
        parent = self.parent if self.parent else ""
        parentIdx = boneTable.get(self.parent, -1)
        matflat = [float(x) for x in self.bindmat.split(' ')]
        mat = np.array([matflat[0:3], matflat[3:6], matflat[6:9]])
        quat = quaternion.from_rotation_matrix(mat)
        (qx, qy, qz, qw) = quaternion.as_float_array(quat)
        (px, py, pz) = [float(x) for x in self.bindpos.split(' ')]
        return f'\t"{self.name}"\t{parentIdx} ( {px:.10f} {py:.10f} {pz:.10f} ) ({qx:.10f} {qy:.10f} {qz:.10f})\t\t// {parent}'
