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

metadata = {
    "apptainer": {"options": "version"},
    "bamtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "bedtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "bowtie": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "bowtie2": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "bwa": {"parser": lambda x: x.stderr.strip().split("\n")[1].split()[1], "citation": "undefined"},
    "cutadapt": {"options": "--version"},
    "deeptools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "DESeq2": {
        "caller": "Rscript -e \"library(DESeq2)\\npackageVersion('DESeq2')\"",
        "parser": lambda x: x.stdout.split()[1].strip("’‘"),
    },
    "fastqc": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "fastp": {"options": "--version", "parser": lambda x: x.stderr.split()[1]},
    "featureCounts": {"parser": lambda x: x.stderr.split("\n")[1].split()[1], "citation": "undefined"},
    "freebayes": {"options": "--version", "parser": lambda x: x.stdout.split()[1][1:]},
    "gffread": {"options": "--version"},
    "kallisto": {"options": "version", "parser": lambda x: x.stdout.split()[2]},
    "minimap2": {"options": "--version"},
    "multiqc": {"options": "--version", "parser": lambda x: x.stdout.split()[2]},
    "salmon": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "samtools": {"options": "--version", "parser": lambda x: x.stdout.split()[1]},
    "seqtk": {"parser": lambda x: x.stderr.split("\n")[2].split()[1], "citation": "undefined"},
    "singularity": {"options": "version"},
    "STAR": {"options": "--version"},
    "snpEff": {"options": "-version", "parser": lambda x: x.stdout.split()[1]},
}
