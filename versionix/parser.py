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

metadata = {
    "apptainer": {"options": "version"},
    "singularity": {"options": "version"},
    "gffread": {"options": "--version"},
    "STAR": {"options": "--version"},
    "minimap2": {"options": "--version"},
    "cutadapt": {"options": "--version"},
    "bwa": {"parser": lambda x: x.stderr.strip().split("\n")[1].split()[1], "citation": "undefined"},
    "seqtk": {"parser": lambda x: x.stderr.split("\n")[2].split()[1], "citation": "undefined"},
    "featureCounts": {"parser": lambda x: x.stderr.split("\n")[1].split()[1], "citation": "undefined"},
    "bamtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "samtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "snpEff": {"options": "-version", "parser": lambda x: x.stdout.split()[1]},
    "deeptools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "salmon": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "fastp": {"options": "--version", "parser": lambda x: x.stderr.split()[1]},
    "bedtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "freebayes": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "fastqc": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "bowtie": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "bowtie2": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "multiqc": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "kallisto": {"options": "version", "parser": lambda x: x.stdout.split()[2]},
    "DESeq2": {
        "caller": "Rscript -e \"library(DESeq2)\\npackageVersion('DESeq2')\"",
        "parser": lambda x: x.stdout.split()[1].strip("’‘"),
    },
}


def get_version(standalone, debug=False):
    """Main entry point that returns the version of an existing executable"""
    # we use check_output in case the standalone opens a GUI (e.g. fastqc --WRONG pops up the GUI)

    try:
        meta = metadata[standalone]
    except Exception as err:
        print("# INFO Your input standalone is not registered. Please provide a PR or fill an issue")
        sys.exit(1)

    # If there is not a special caller defined, let us check that the standalone exists
    if "caller" not in meta.keys() and shutil.which(standalone) is None:
        print(f"ERROR: {standalone} command not found in your environment")
        sys.exit(1)

    # The command used to get the version output
    caller = meta.get("caller", standalone)
    # The options necessary to get the version output
    options = meta.get("options", "")
    # The parser of the version output
    parser = meta.get("parser", lambda x: x.stdout.strip())

    try:
        cmd = f"{caller} {options}"

        p = subprocess.run(cmd, capture_output=True, universal_newlines=True, shell=True)
        version = parser(p)
        return version

    except Exception as err:
        print(err)
        sys.exit(1)
