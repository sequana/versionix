from versionix.parser import get_version
from versionix.scripts import main

import sys


def test_kallisto(fp):
    fp.register(["kallisto", "version"], stdout=["kallisto, version 0.48.0"])
    assert get_version("kallisto") == "0.48.0"


def _test_bwa(fp):
    fp.register(
        ["bwa"],
        stderr=[
            """
Program: bwa (alignment via Burrows-Wheeler transformation)
Version: 0.7.17-r1188
Contact: Heng Li <lh3@sanger.ac.uk>

Usage:   bwa <command> [options]
"""
        ],
    )
    assert get_version("bwa") == "0.7.17-r1188"


def test_bedtools(fp):
    fp.register(["bedtools", "--version"], stdout=["bedtools v2.30.0"])
    assert get_version("bedtools") == "2.30.0"


def test_bamtools(fp):
    fp.register(["bamtools", "--version"], stdout=["bamtools 2.5.2"])
    assert get_version("bamtools") == "2.5.2"


def test_singularity(fp):
    fp.register(["singularity", "version"], stdout=["3.6.2+12-gad3457a9a"])
    assert get_version("singularity") == "3.6.2+12-gad3457a9a"


def test_script(fp):
    from click.testing import CliRunner

    runner = CliRunner()

    fp.register(["bedtools", "--version"], stdout=["bedtools v2.30.0"])

    # sys.argv = ["bedtools"]
    result = runner.invoke(main, ["bedtools"])
    assert result.exit_code == 0
