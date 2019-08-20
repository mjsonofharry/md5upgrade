import re

class Vert:
    Pattern = re.compile(r'vert .+')
    ValPattern = re.compile(r'(\d+) (-?\d+\.?\d+) (-?\d+\.?\d+) (\d+) (\d+)')

    def __init__(self, vertbuf):
        self.values = Vert.ValPattern.search(vertbuf).groups()
        
    def convert(self):
        vertIndex, s, t, startWeight, counterWeight = [v for v in self.values]
        return f'\tvert {vertIndex} ( {s} {t} ) {startWeight} {counterWeight}'


class Tri:
    Pattern = re.compile(r'(tri .+)')

    def __init__(self, tribuf):
        self.values = tribuf

    def convert(self):
        return f'\t{self.values}'


class Weight:
    Pattern = re.compile(r'weight .+')
    ValPattern = re.compile(r'(\d+) (\d+) (-?\d+\.?\d+) ((?:-?\d+\.?\d+\s*){3})')

    def __init__(self, weightbuf):
        self.values = Weight.ValPattern.search(weightbuf).groups()
    
    def convert(self):
        index, joint, bias, position = self.values
        return f'\tweight {index} {joint} {bias} ( {position} )'


class Mesh:
    Pattern = re.compile(r'mesh \d+ {[\s\S]*?}')
    ShaderPattern = re.compile(r'shader ".+\/(models\/.+)\.\w+"')
    
    NumVertsPattern = re.compile(r'numverts (\d+)')
    NumTrisPattern = re.compile(r'numtris (\d+)')
    NumWeightsPattern = re.compile(r'numweights (\d+)')

    def __init__(self, meshbuf):
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
\t//meshes: {''}
\tshader "{self.shader}"

\tnumverts {self.numverts}
{verts}

\tnumtris {self.numtris}
{tris}

\tnumweights {self.numweights}
{weights}
{rcurl}
'''