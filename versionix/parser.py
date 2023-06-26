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
    """versionix, version 0.1.0"""
    raise NotImplementedError


def parser_Version_column_version(stdout: str, *args):
    """

    Version: v1.0.0

    """
    for line in stdout.split("\n"):
        if line.startswith("Version:"):
            return line.strip().split(":", 1)[1].strip()


def parser_standalone_version(stdout: str, standalone, *args):
    """

    STANDALONE: 1.0.0

    """
    for line in stdout.split("\n"):
        if line.startswith(f"{standalone}"):
            return line.strip().split()[1].strip()


metadata = {
    "default": {"caller": "--version", "parser": None, "citation": "undefined"},
    "bwa": {"caller": "stderr", "parser": parser_Version_column_version, "citation": "undefined"},
    "bamtools": {"caller": "--version", "parser": parser_standalone_version}
    # "art_454":{
    #    "caller": "stdout",
    #    "parser":  parser_name_Version_version
    # }
}


def base_version_parser(stdout: str):
    """{NAME}: v1.0.0"""
    return stdout.split("\n", 1)[0].split()[-1]


def seqtk_version_parser(stderr: str):
    return stderr.strip().split("\n")[1].split()[-1]


def get_version_method_long_argument(standalone):

    try:
        # Try --version flag first
        command = [standalone, "--version"]
        output = subprocess.check_output(command, stderr=subprocess.PIPE, universal_newlines=True)
        return output

    except subprocess.CalledProcessError as e:
        # --version flag not available, try other flags
        # error_message = e.stderr.strip()
        # if error_message:
        #    return error_message
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

    # Try -v flag
    try:
        command = [standalone, "version"]
        output = subprocess.check_output(command, stderr=subprocess.PIPE, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        pass


# =========================================================================


def get_version(standalone, debug=False):
    # we use check_output in case the standalone opens a GUI (e.g. fastqc --WRONG pops up the GUI)

    # Let us checl that the standalone exists
    if shutil.which(standalone) is None:
        print(f"ERROR: {standalone} command not found in your environment")
        sys.exit(1)

    # Now, what kind of caller and parser do we need ?

    meta = metadata.get(standalone, metadata.get("default"))

    # Case when the standalone prints information on stderr
    # e.g. bwa
    if meta["caller"] == "stderr":
        command = [standalone]
        try:
            resp = subprocess.run([standalone], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            return meta["parser"](resp.stderr, standalone)
        except subprocess.CalledProcessError as e:
            print(e)
            pass

    # bamtools hides the --version and then prints somewhere: "bamtools 1.0.0"
    #
    version = get_version_method_long_argument(standalone)
    if meta["parser"]:
        return meta["parser"](version, standalone)
    elif version:
        return version

    version = get_version_method_short_argument(standalone)
    if meta["parser"]:
        return meta["parser"](version)
    elif version:
        return version

    version = get_version_method_subcommand(standalone)
    if meta["parser"]:
        return meta["parser"](version)
    elif version:
        return version

    # If none of the flags work, return an error message
    return "Unable to retrieve version information"
