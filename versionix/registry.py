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

# default parser performs stdout.strip()

# versionix 1.0.0
parser_split_2 = lambda x: x.stdout.split()[1]

# versionix v1.0.0
parser_split_2_strip_v = lambda x: x.stdout.split()[1][1:]

# versionix version 1.0.0
parser_split_3 = lambda x: x.stdout.split()[2]


metadata = {
    "apptainer": {
        "options": "version"
    },
    "bamtools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "bedtools": {
        "options": "--version", 
        "parser": parser_split_2_strip_v
    },
    "bowtie": {
        "options": "--version", 
        "parser": parser_split_3
    },
    "bowtie2": {
        "options": "--version",
        "parser": parser_split_3
    },
    "bwa": {
        "parser": lambda x: x.stderr.strip().split("\n")[1].split()[1]
    },
    "cutadapt": {
        "options": "--version"
    },
    "deeptools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "DESeq2": {
        "caller": "Rscript -e \"library(DESeq2)\\npackageVersion('DESeq2')\"",
        "parser": lambda x: x.stdout.split()[1].strip("’‘"),
    },
    "fastqc": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "fastp": {
        "options": "--version", 
        "parser": parser_split_2
    },
    "featureCounts": {
        "options": "-v",
        "parser": lambda x: x.stderr.split("\n")[1].split()[1], 
    },
    "freebayes": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "gffread": {
        "options": "--version"
    },
    "jellyfish": {
        "options": "--version",
        "parser": parser_split_2
    },
    "kallisto": {
        "options": "version",
        "parser": parser_split_3
    },
    "kraken2": {
        "options": "--version",
        "parser": parser_split_3
    },
    "macs3": {
        "options": "--version",
        "parser": parser_split_2,
    },
    "minimap2": {
        "options": "--version"
    },
    "multiqc": {
        "options": "--version",
        "parser": parser_split_3
    },
    "plotCorrelation": {
        "options": "--version",
        "parser": parser_split_2
    },
    "plotFingerprint": {
        "options": "--version",
        "parser": parser_split_2
    },
    "salmon": {
        "options": "--version",
        "parser": parser_split_2
    },
    "samtools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "seqtk": {
        "parser": lambda x: x.stderr.split("\n")[2].split()[1]
    },
    "singularity": {
        "options": "version"
    },
    "STAR": {
        "options": "--version"
    },
    "snpEff": {
        "options": "-version", 
        "parser": parser_split_2
    },
}
