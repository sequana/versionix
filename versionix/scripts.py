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
""".. rubric:: Standalone application (CLI entry point) for Versionix"""
import sys

import colorlog
import rich_click as click

from versionix import version
from versionix.parser import get_version

__all__ = ["main"]

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

click.rich_click.TEXT_MARKUP = "markdown"
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.SHOW_ARGUMENTS = True

logger = colorlog.getLogger(__name__)


@click.command()
@click.argument("standalone", required=False, type=click.STRING, default=None)
@click.version_option(version)
@click.option("--registered", is_flag=True, help="Prints the list of registered tools")
@click.option(
    "--logger-level",
    type=click.Choice(["INFO", "DEBUG", "WARNING", "ERROR"]),
    help="level for debugging",
    default="INFO",
)
@click.option(
    "--from",
    "from_container",
    default=None,
    type=click.STRING,
    help="Container image to introspect (e.g., a Singularity/Apptainer .img/.sif file or a Docker image name)",
)
def main(**kwargs):
    """Versionix returns the version of bioinformatics software.

    ----

        versionix fastqc

    You can check the list of registered tools as follows

        versionix --registered

    You can retrieve the version of a tool from inside a container

        versionix sequana_coverage --from sequana_0.18.img

    """

    from versionix import logger

    logger._set_level(kwargs["logger_level"])

    if kwargs["registered"]:
        from versionix.registry import metadata

        names = sorted(metadata.keys())
        for name in names:
            click.echo(f"{name}")
    else:
        if kwargs["standalone"] is None:
            from rich.panel import Panel
            from rich.console import Console

            console = Console()
            console.print(
                Panel(
                    f"[bold blue]versionix[/bold blue] [cyan]v{version}[/cyan]\n\n"
                    "[white]Authors: Sequana Team[/white]\n"
                    "[white]Repository: https://github.com/sequana/versionix[/white]\n\n"
                    "[italic]Get the version of any bioinformatics tool.[/italic]\n\n"
                    "[yellow]Usage:[/yellow] versionix <standalone>\n"
                    "[yellow]Help:[/yellow]  versionix --help",
                    title="[bold]Versionix[/bold]",
                    expand=False,
                )
            )
            sys.exit(0)
        else:
            click.echo(get_version(kwargs["standalone"], container=kwargs["from_container"]))
