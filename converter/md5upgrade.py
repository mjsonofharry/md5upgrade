import re
import sys

from bone import Bone
from mesh import Mesh

MD5VersionPattern = re.compile(r'MD5Version (\d+)')
CommandLinePattern = re.compile(r'commandline (".*")')
NumBonesPattern = re.compile(r'numbones (\d+)')
NumMeshesPattern = re.compile(r'nummeshes (\d+)')

def convert(md5v6):
    md5version = MD5VersionPattern.search(md5v6).group(1)
    assert md5version == '6'
    commandline = CommandLinePattern.search(md5v6).group(1)

    numbones = NumBonesPattern.search(md5v6).group(1)
    bones = sorted([Bone(b) for b in Bone.Pattern.findall(md5v6)], key=lambda x: x.index)
    for i,b in enumerate(bones): assert b.index == i
    boneTable = {b.name: b.index for b in bones}
    numJoints = len(bones)
    joints = '\n'.join([b.convert(boneTable) for b in bones])

    nummeshes = NumMeshesPattern.search(md5v6).group(1)
    meshes = '\n'.join([Mesh(m).convert() for m in Mesh.Pattern.findall(md5v6)])

    lcurl = '{'
    rcurl = '}'

    return f'''MD5Version 10
commandline {commandline}

numJoints {numJoints}
numMeshes {nummeshes}

joints {lcurl}
{joints}
{rcurl}

{meshes}
'''

def main():
    fin_path = sys.argv[1]
    fout_path = sys.argv[2]
    with open(fin_path, 'r') as fin, open(fout_path, 'w') as fout:
        md5v6 = fin.read()
        md5v10 = convert(md5v6)
        fout.write(md5v10)

if __name__ == '__main__':
    main()