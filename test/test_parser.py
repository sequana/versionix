from versionix.parser import get_version




def test_bwa(fp):

    fp.register(["bwa"], stderr=["""
Program: bwa (alignment via Burrows-Wheeler transformation)
Version: 0.7.17-r1188
Contact: Heng Li <lh3@sanger.ac.uk>

Usage:   bwa <command> [options]
"""])
    assert  get_version("bwa") == "0.7.17-r1188"


def test_bedtools(fp):
    fp.register(["bedtools", "--version"], stdout=["bedtools v2.30.0"])
    assert  get_version("bedtools") == "v2.30.0"


def test_bamtools(fp):
    fp.register(["bamtools", "--version"], stdout=["bamtools 2.5.2"])
    assert  get_version("bamtools") == "2.5.2"
