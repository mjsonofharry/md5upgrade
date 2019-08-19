import re
import scipy

MD5VersionPattern = re.compile(r'MD5Version (\d+)')
CommandLinePattern = re.compile(r'commandline (".*")')
NumBonesPattern = re.compile(r'numbones (\d+)')
NumMeshesPattern = re.compile(r'nummeshes (\d+)')

BonePattern = re.compile(r'bone \d+ {[\s\S]*?}')
MeshPattern = re.compile(r'mesh \d+ {[\s\S]*?}')

NamePattern = re.compile(r'name "(\w+)"')
BindPosPattern = re.compile(r'bindpos ((?:-?\d+\.?\d* ?){3})')
BindMatPattern = re.compile(r'bindmat ((?:-?\d+\.?\d* ?){9})')
ParentPattern = re.compile(r'parent "(\w+)"')

class Joint:
    def __init__(self, idx, bone):
        self.name = NamePattern.search(bone).group(1)
        self.bindpos = BindPosPattern.search(bone).group(1)
        self.bindmat = BindMatPattern.search(bone).group(1)
        maybeParent = ParentPattern.search(bone)
        self.parent = maybeParent.group(1) if maybeParent else None
        self.idx = idx

    def to_str(self, jointTable):
        parentIdx = jointTable.get(self.parent, -1)
        m = [float(x) for x in self.bindmat.split(' ')]
        q = scipy.spatial.transform.Rotation.from_dcm([m[0:3], m[3:6], m[6:9]]).as_quat() * -1
        return f'"{self.name}"    {parentIdx} ( {bindpos} ) ({q[0]} {q[1]} {q[2]})'

def convert(md5v6: str):
    md5version = MD5VersionPattern.search(md5v6).group(1)
    commandline = CommandLinePattern.search(md5v6).group(1)
    numbones = NumBonesPattern.search(md5v6).group(1)
    nummeshes = NumMeshesPattern.search(md5v6).group(1)

    joints = [Joint(i,b) for i,b in enumerate(BonePattern.findall(md5v6))]
    jointTable = {j.name: j.idx for j in joints}

    #meshes = [Mesh(m) for m in MeshPattern.findall(md5v6)]

def main():
    md5v6 = open('md5v6.txt', 'r')
    result = convert(md5v6)