import sys

from versionix.parser import get_version as get_version
from versionix.scripts import main

# for testing we do not want to install all those tools/software so
# we have set testing=True, in which case some sanity checks and
# error won't be raised.
# def get_version(standalone):
#    return get_version_orig(standalone, testing=True)

# The mocker which is set so that when we test the presence of e.G. macs3, which is not installed,
# no error is raise


def test_sequana(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["sequana_coverage", "--version"], stdout=["sequana_coverage, version 0.15.4"])
    assert get_version("sequana_coverage") == "0.15.4"


def test_macs3(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["macs3", "--version"], stdout=["macs3 3.0.0b1"])
    assert get_version("macs3") == "3.0.0b1"


def test_pigz(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["pigz", "--version"], stdout=["pigz 2.4"])
    assert get_version("pigz") == "2.4"


def test_fastqc(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["fastqc", "--version"], stdout=["FastQC v1.0.0"])
    assert get_version("fastqc") == "1.0.0"


def test_bwa(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["bwa", "--version"], stdout=[], stderr=["[main] unrecognized command '--version'"])
    fp.register(["bwa", "-v"], stdout=[], stderr=["[main] unrecognized command '-v'"])
    fp.register(["bwa", "version"], stdout=[], stderr=["[main] unrecognized command 'version'"])
    fp.register(["bwa", "-V"], stdout=[], stderr=["[main] unrecognized command '-V'"])
    fp.register(["bwa", "-version"], stdout=[], stderr=["[main] unrecognized command '-version'"])
    fp.register(
        ["bwa"],
        stdout=[],
        stderr=[
            """

Program: bwa (alignment via Burrows-Wheeler transformation)
Version: 0.7.17-r1188
Contact: Heng Li <lh3@sanger.ac.uk>

Usage:   bwa <command> [options]
"""
        ],
        returncode=1,
    )
    assert get_version("bwa") == "0.7.17"


def test_blacklists(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    assert get_version("Build_Trinotate_Boilerplate_SQLite_db.pl") == "?.?.?"


def test_bedtools(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["bedtools", "--version"], stdout=["bedtools v2.30.0"])
    assert get_version("bedtools") == "2.30.0"


def test_bamtools(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["bamtools", "--version"], stdout=["bamtools 2.5.2"])
    assert get_version("bamtools") == "2.5.2"


def test_singularity(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    fp.register(["singularity", "--version"], stdout=["apptainer version 1.3.1-1.fc40"])
    fp.register(["singularity", "version"], stdout=["1.3.1-1.fc403"])
    assert get_version("singularity") == "1.3.1"


def test_registered(fp, mocker):
    mocker.patch("shutil.which", return_value="something")
    # fp.register(["dot", "--version"], stdout=["dot - graphviz version 2.40.1 (20161225.0304)"])
    fp.register(["dot", "-V"], stderr=["dot - graphviz version 2.40.1 (20161225.0304)"])
    assert get_version("dot") == "2.40.1"


def test_script(fp, mocker):
    from click.testing import CliRunner

    runner = CliRunner()

    fp.register(["bedtools", "--version"], stdout=["bedtools v2.30.0"])
    mocker.patch("shutil.which", return_value="bedtools")

    result = runner.invoke(main, ["bedtools"])
    print(result)

    runner.invoke(main, ["--registered"])
    runner.invoke(
        main,
    )


def test_DESeq2_error(fp, mocker):
    # registered tool but if not installed, should raise a SystemExit error
    try:
        mocker.patch("shutil.which", return_value=None)
        get_version("DESeq2")
        assert False
    except SystemExit:
        assert True


def test_DESeq2_uses_rscript_caller(fp, mocker):
    # DESeq2 is registered with a Rscript caller; the PATH check should look for Rscript, not DESeq2
    def which_side_effect(cmd):
        return "/usr/bin/Rscript" if cmd == "Rscript" else None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    fp.register(
        'Rscript -e "library(DESeq2);packageVersion(\'DESeq2\')"',
        stdout=["[1] '1.42.0'"],
    )
    assert get_version("DESeq2") == "1.42.0"


def test_empty_parsers(fp, mocker):
    try:
        mocker.patch("shutil.which", return_value=True)
        get_version("for_testing_empty_parsers")
        assert False
    except ValueError:
        assert True


def test_no_parser(fp, mocker):
    try:
        mocker.patch("shutil.which", return_value=True)
        get_version("for_testing_no_parsers")
        assert False
    except ValueError:
        assert True


def test_from_singularity_img(fp, mocker):
    # shutil.which returns "singularity" when asked for singularity/apptainer runners
    def which_side_effect(cmd):
        if cmd == "apptainer":
            return None
        if cmd == "singularity":
            return "/usr/bin/singularity"
        return None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    fp.register(
        ["singularity", "exec", "sequana_0.18.img", "sequana_coverage", "--version"],
        stdout=["sequana_coverage, version 0.15.4"],
    )
    assert get_version("sequana_coverage", container="sequana_0.18.img") == "0.15.4"


def test_from_apptainer_sif(fp, mocker):
    def which_side_effect(cmd):
        if cmd == "apptainer":
            return "/usr/bin/apptainer"
        return None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    fp.register(
        ["apptainer", "exec", "myimage.sif", "fastqc", "--version"],
        stdout=["FastQC v0.12.0"],
    )
    assert get_version("fastqc", container="myimage.sif") == "0.12.0"


def test_from_docker_image(fp, mocker):
    def which_side_effect(cmd):
        if cmd == "docker":
            return "/usr/bin/docker"
        return None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    mocker.patch("versionix.parser.os.path.isfile", return_value=False)
    fp.register(
        ["docker", "run", "--rm", "myimage:latest", "fastqc", "--version"],
        stdout=["FastQC v0.12.0"],
    )
    assert get_version("fastqc", container="myimage:latest") == "0.12.0"


def test_from_registered_tool_with_container(fp, mocker):
    def which_side_effect(cmd):
        if cmd == "apptainer":
            return None
        if cmd == "singularity":
            return "/usr/bin/singularity"
        return None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    fp.register(
        ["singularity", "exec", "sequana_0.18.img", "dot", "-V"],
        stderr=["dot - graphviz version 2.40.1 (20161225.0304)"],
    )
    assert get_version("dot", container="sequana_0.18.img") == "2.40.1"


def test_script_from_container(fp, mocker):
    from click.testing import CliRunner

    def which_side_effect(cmd):
        if cmd == "apptainer":
            return None
        if cmd == "singularity":
            return "/usr/bin/singularity"
        return None

    mocker.patch("versionix.parser.shutil.which", side_effect=which_side_effect)
    fp.register(
        ["singularity", "exec", "sequana_0.18.img", "sequana_coverage", "--version"],
        stdout=["sequana_coverage, version 0.15.4"],
    )

    runner = CliRunner()
    result = runner.invoke(main, ["sequana_coverage", "--from", "sequana_0.18.img"])
    assert "0.15.4" in result.output
