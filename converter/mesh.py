import re

from util import formatValue, Vector

class Vert:
    Pattern = re.compile(r'vert .+')

    def __init__(self, vertbuf):
        label, index, s, t, startWeight, counterWeight = vertbuf.split(' ')
        assert label == 'vert'
        self.index = int(index)
        self.textureU = float(s)
        self.textureV = float(t)
        self.startWeight = int(startWeight)
        self.counterWeight = int(counterWeight)

        
    def convert(self):
        return f'\tvert {self.index} ( {formatValue(self.textureU)} {formatValue(self.textureV)} ) {self.startWeight} {self.counterWeight}'


class Tri:
    Pattern = re.compile(r'(tri .+)')

    def __init__(self, tribuf):
        self.data = tribuf
        assert self.data.split(' ')[0] == 'tri'

    def convert(self):
        return f'\t{self.data}'


class Weight:
    Pattern = re.compile(r'weight .+')

    def __init__(self, weightbuf):
        label, index, joint, bias, x, y, z = weightbuf.split(' ')
        assert label == 'weight'
        self.index = int(index)
        self.joint = int(joint)
        self.bias = float(bias)
        self.position = Vector(float(x), float(y), float(z))
    
    def convert(self):
        return f'\tweight {self.index} {self.joint} {formatValue(self.bias)} ( {formatValue(self.position.x)} {formatValue(self.position.y)} {formatValue(self.position.z)} )'


class Mesh:
    Pattern = re.compile(r'mesh \d+ {[\s\S]*?}')
    IndexPattern = re.compile(r'mesh (\d) {')
    ShaderPattern = re.compile(r'shader ".+\/(models\/.+)\.\w+"')
    
    NumVertsPattern = re.compile(r'numverts (\d+)')
    NumTrisPattern = re.compile(r'numtris (\d+)')
    NumWeightsPattern = re.compile(r'numweights (\d+)')

    def __init__(self, meshbuf):
        self.index = Mesh.IndexPattern.search(meshbuf).group(1)
        self.shader = Mesh.ShaderPattern.search(meshbuf).group(1)
        self.numverts = Mesh.NumVertsPattern.search(meshbuf).group(1)
        self.numtris = Mesh.NumTrisPattern.search(meshbuf).group(1)
        self.numweights = Mesh.NumWeightsPattern.search(meshbuf).group(1)
        self.verts = [Vert(v) for v in Vert.Pattern.findall(meshbuf)]
        self.tris = [Tri(t) for t in Tri.Pattern.findall(meshbuf)]
        self.weights = [Weight(w) for w in Weight.Pattern.findall(meshbuf)]

    def convert(self):
        verts = '\n'.join([v.convert() for v in self.verts])
        tris = '\n'.join([t.convert() for t in self.tris])
        weights = '\n'.join([w.convert() for w in self.weights])

        lcurl = '{'
        rcurl = '}'

        return f'''mesh {lcurl}
\t// meshes: {self.shader.split('/')[-1]}
\tshader "{self.shader}"

\tnumverts {self.numverts}
{verts}

\tnumtris {self.numtris}
{tris}

\tnumweights {self.numweights}
{weights}
{rcurl}
'''