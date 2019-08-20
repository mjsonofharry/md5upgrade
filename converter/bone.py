import re
from scipy.spatial.transform import Rotation

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
        m = [float(x) for x in self.bindmat.split(' ')]
        q_x, q_y, q_z, q_w = Rotation.from_dcm([m[0:3], m[3:6], m[6:9]]).as_quat() * -1
        return f'\t"{self.name}"\t{parentIdx} ( {self.bindpos} ) ({q_x} {q_y} {q_z})\t\t// {parent}'