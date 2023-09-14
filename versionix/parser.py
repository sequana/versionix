#
#  This file is part of Versionix software
#
#  Copyright (c) 2023 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/versionix
#  Contributors:  https://github.com/sequana/versionix/graphs/contributors
##############################################################################

import shutil
import subprocess
import sys


def parse_click():
    """one liner output

    versionix, version 0.1.0

    """
    raise NotImplementedError


def parse_standalone_version_version(stdout: str):
    """one liner output

    singularity version 3.6.2+12-gad3457a9a

    """
    return stdout.strip().split()


def parser_Version_column_version(stdout: str, *args):
    """

    Version: v1.0.0

    """
    for line in stdout.split("\n"):
        if line.startswith("Version:"):
            return line.strip().split(":", 1)[1].strip()


def parser_standalone_version(stdout: str, standalone, *args):
    """

    STANDALONE 1.0.0

    """
    for line in stdout.split("\n"):
        if line.startswith(f"{standalone}"):
            return line.strip().split()[1].strip()

metadata = {
    "bwa": {"caller": "stderr", "parser": parser_Version_column_version, "citation": "undefined"},
    "seqtk": {"caller": "stderr", "parser": parser_Version_column_version, "citation": "undefined"},
    "bamtools": {"caller": "--version", "parser": parser_standalone_version},
    "singularity": {"caller": "version", "parser": None},
    "bedtools": {"caller": "--version", "parser": parser_standalone_version},
    "deeptools": {"caller": "--version", "parser": parser_standalone_version},
    "salmon": {"caller": "--version", "parser": parser_standalone_version},
    "gffread": {"caller": "--version", "parser": None},
    "bamtools": {"caller": "--version", "parser": parser_standalone_version}
}


def get_version_method_long_argument(standalone):

    try:
        # Try --version flag first
        command = [standalone, "--version"]
        output = subprocess.check_output(command, stderr=subprocess.PIPE, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        pass


def get_version_method_short_argument(standalone):

    # Try -v flag
    try:
        command = [standalone, "-v"]
        output = subprocess.check_output(command, stderr=subprocess.PIPE, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        pass


def get_version_method_subcommand(standalone):

    # Try subcommand
    try:
        command = [standalone, "version"]
        output = subprocess.check_output(command, stderr=subprocess.PIPE, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        pass


# =========================================================================


def get_version(standalone, debug=False):
    """Main entry point that returns the version of an existing executable"""
    # we use check_output in case the standalone opens a GUI (e.g. fastqc --WRONG pops up the GUI)

    # Let us checl that the standalone exists
    if shutil.which(standalone) is None:
        print(f"ERROR: {standalone} command not found in your environment")
        sys.exit(1)

    # Now, what kind of caller and parser do we need ?
    try:
        meta = metadata[standalone]
    except Exception as err:
        print("# INFO Your input standalone is not registered. Please provide a PR or fill an issue")
        sys.exit(1)


    # Case when the standalone prints information on stderr
    # e.g. bwa, seqtk
    if meta["caller"] == "stderr":
        command = [standalone]
        try:
            resp = subprocess.run([standalone], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            return meta["parser"](resp.stderr, standalone)
        except subprocess.CalledProcessError as e:
            print(e)
            pass
    elif meta['caller'] == 'version':
        version = get_version_method_subcommand(standalone)
        if meta["parser"]:
            return meta["parser"](version)
        elif version:
            return version
    elif meta['caller'] == '--version':
        version = get_version_method_long_argument(standalone)
        if meta["parser"]:
            return meta["parser"](version, standalone)
        elif version:
            return version
    elif meta['caller'] == 'standalone':
        version = get_version_method_subcommand(standalone)
        if meta["parser"]:
            return meta["parser"](version)
        elif version:
            return version
