import numpy as np
import re
from scipy.spatial.transform import Rotation

from util import formatValue, Vector

class Bone:
    Pattern = re.compile(r'bone \d+ {[\s\S]*?}')

    def parseIndex(line):
        line = [w.strip() for w in line.split(' ') if w]
        label, index = line[:2]
        assert label == 'bone'
        return int(index)

    def parseName(line):
        line = [w.strip() for w in line.split(' ') if w]
        label, name = line[:2]
        assert label == 'name'
        return name.replace('"', '')

    def parseBindpos(line):
        line = [w.strip() for w in line.split(' ') if w]
        label, pos = line[0], [float(v) for v in line[1:]]
        assert label == 'bindpos'
        assert len(pos) == 3
        return Vector(*pos)

    def parseBindmat(line):
        line = [w.strip() for w in  line.split(' ') if w]
        label, bindmat = line[0], [float(v) for v in line[1:]]
        assert label == 'bindmat'
        assert len(bindmat) == 9
        return [bindmat[0:3], bindmat[3:6], bindmat[6:9]]

    def parseParent(line: str) -> str:
        line = [w.strip() for w in line.split(' ') if w]
        label = line[0]
        return line[1].replace('"', '') if label == 'parent' else None

    def __init__(self, bonebuf): 
        data = bonebuf.splitlines()
        assert len(data) >= 4
        self.index = Bone.parseIndex(data[0])
        self.name = Bone.parseName(data[1])
        self.bindpos = Bone.parseBindpos(data[2])
        self.bindmat = Bone.parseBindmat(data[3])
        self.parent = Bone.parseParent(data[4])

    def convert(self, boneTable):
        position = f'{formatValue(self.bindpos.x)} {formatValue(self.bindpos.y)} {formatValue(self.bindpos.z)}'
        parentName = self.parent if self.parent else ""
        parentIndex = boneTable.get(self.parent, -1)
        q = Vector(*Rotation.from_dcm(np.array(self.bindmat)).as_quat())
        orientation = f'{formatValue(q.x)} {formatValue(q.y)} {formatValue(q.z)}'
        return f'\t"{self.name}"\t{parentIndex} ( {position} ) ( {orientation} )\t\t// {parentName}'
