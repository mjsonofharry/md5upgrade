import os
import re
import sys

from bone import Bone
from mesh import Mesh

MD5VersionPattern = re.compile(r'MD5Version (\d+)')
CommandLinePattern = re.compile(r'commandline (".*")')
NumBonesPattern = re.compile(r'numbones (\d+)')
NumMeshesPattern = re.compile(r'nummeshes (\d+)')

def convert(md5v6: str) -> str:
    md5version = MD5VersionPattern.search(md5v6).group(1)
    assert md5version == '6'
    commandline = CommandLinePattern.search(md5v6).group(1)

    numbones = NumBonesPattern.search(md5v6).group(1)
    bones = sorted([Bone(b) for b in Bone.Pattern.findall(md5v6)], key=lambda x: x.index)
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

def convert_io(input_path: str, output_path: str):
    print(f'Reading "{input_path}" and writing "{output_path}"')
    if not os.path.exists(input_path):
        print(f'Error: cannot read "{input_path}" because it does not exist.')
        sys.exit(1)
    if not os.path.isfile(input_path):
        print(f'Error: cannot read "{input_path}" because it is not a file.')
        sys.exit(1)
    if os.path.exists(output_path):
        answer = input(f'Warning: this will overwrite "{output_path}". Continue? [y/n]: ')
        if answer.lower() != 'y':
            print('Terminating')
            sys.exit(0)
    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        md5v6 = fin.read()
        md5v10 = convert(md5v6)
        fout.write(md5v10)

def main():
    source = os.path.abspath(sys.argv[1])
    destination = os.path.abspath(sys.argv[2])
    if os.path.isdir(source):
        if not os.path.isdir(destination):
            print(f'Error: cannot use "{destination} as output for batch conversion because it is not a directory')
            sys.exit(1)
        for fname in os.listdir(source):
            if not fname.endswith('.md5mesh'):
                continue
            input_path = os.path.join(source, fname)
            output_path = os.path.join(destination, fname)
            convert_io(input_path, output_path)
    else:
        if os.path.isdir(destination):
            fname = os.path.basename(source)
            output_path = os.path.join(destination, fname)
            convert_io(source, output_path)
        else:
            convert_io(source, destination)


if __name__ == '__main__':
    main()