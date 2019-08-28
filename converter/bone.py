import numpy as np
import re
import sys

from nibabel import quaternions
from dataclasses import dataclass

from util import formatValue, Vector

class _Bone:
    Pattern = re.compile(r'bone \d+ {[\s\S]*?}')

    def parseIndex(line):
        line = [w.strip() for w in line.split(' ') if w]
        label, index = line[0], int(line[1])
        if label != 'bone':
            sys.exit(1)
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
        label = line[0]
        bindmat = [float(v) for v in line[1:]]
        assert label == 'bindmat'
        assert len(bindmat) == 9
        return [bindmat[0:3], bindmat[3:6], bindmat[6:9]]

    def parseParent(line: str) -> str:
        line = [w.strip() for w in line.split(' ') if w]
        label = line[0]
        return line[1].replace('"', '') if label == 'parent' else None

    def __init__(self, index: int, bonebuf: str): 
        data = bonebuf.splitlines()
        assert len(data) >= 4
        self.index = Bone.parseIndex(data[0])
        assert index == self.index
        self.name = Bone.parseName(data[1])
        self.bindpos = Bone.parseBindpos(data[2])
        self.bindmat = Bone.parseBindmat(data[3])
        self.parent = Bone.parseParent(data[4])

    def convert(self, boneTable: dict):
        parentName = self.parent if self.parent else ""
        parentIndex = boneTable.get(parentName, -1)
        px, py, pz = self.bindpos.x, self.bindpos.y, self.bindpos.z
        q = quaternions.mat2quat(np.array(self.bindmat))
        (px, py, pz) = [formatValue(v) for v in self.bindpos.split(' ')]
        (qw, qx, qy, qz) = [formatValue(v) for v in q]
        return f'\t"{self.name}"\t{parentIndex} ( {px} {py} {pz} ) ( {qx} {qy} {qz} )\t\t// {parentName}'

@dataclass
class Bone:
    index: int
    name: str
    bindpos: tuple
    bindmat: list
    parentName: str

@dataclass
class Joint:
    index: int
    name: str
    parentIndex: str
    position: tuple
    orientation: tuple
    parentName: str

