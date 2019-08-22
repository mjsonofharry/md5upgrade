import numpy as np
import re
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import quaternion

from util import simplifyFloat

class Bone:
    Pattern = re.compile(r'bone \d+ {[\s\S]*?}')
    IndexPattern = re.compile(r'bone (\d+)')
    NamePattern = re.compile(r'name "(\w+)"')
    BindPosPattern = re.compile(r'bindpos ((?:-?\d+\.?\d* ?){3})')
    BindMatPattern = re.compile(r'bindmat ((?:-?\d+\.?\d* ?){9})')
    ParentPattern = re.compile(r'parent "(\w+)"')

    def __init__(self, bonebuf):
        self.index = int(Bone.IndexPattern.search(bonebuf).group(1))
        self.name = Bone.NamePattern.search(bonebuf).group(1)
        self.bindpos = Bone.BindPosPattern.search(bonebuf).group(1)
        self.bindmat = Bone.BindMatPattern.search(bonebuf).group(1)
        maybeParent = Bone.ParentPattern.search(bonebuf)
        self.parent = maybeParent.group(1) if maybeParent else None

    def convert(self, boneTable):
        parentName = self.parent if self.parent else ""
        parentIndex = boneTable.get(self.parent, -1)
        matflat = [float(x) for x in self.bindmat.split(' ')]
        mat = np.array([matflat[0:3], matflat[3:6], matflat[6:9]])
        q = quaternion.from_rotation_matrix(mat)
        (px, py, pz) = [simplifyFloat(float(x)) for x in self.bindpos.split(' ')]
        (qx, qy, qz) = [simplifyFloat(round(c, 10)) for c in (q.x, q.y, q.z)]
        return f'\t"{self.name}"\t{parentIndex} ( {px} {py} {pz} ) ({qx} {qy} {qz})\t\t// {parentName}'
