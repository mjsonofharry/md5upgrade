import pytest

from test_utils import SAMPLE_BONE_ORIGIN, SAMPLE_BONE, bone

class TestBone:
    def test_init_origin(self):
        b = bone.Bone(0, SAMPLE_BONE_ORIGIN)
        assert b.name == 'origin'
        assert b.bindpos == '0.000000 0.000000 0.000000'
        assert b.bindmat == '0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 0.000000 0.000000 1.000000'
        assert b.parent == None

    def test_init(self):
        b = bone.Bone(3, SAMPLE_BONE)
        assert b.name == 'Rupleg'
        assert b.bindpos == '-1.229870 -5.413517 50.523598'
        assert b.bindmat == '-0.281509 0.948261 -0.146812 0.085640 -0.127560 -0.988127 -0.955729 -0.290740 -0.045299'
        assert b.parent == 'Hips'
