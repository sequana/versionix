###########################################################################
# Versionix is a project to manage reproducible containers                #
#                                                                         #
# Authors: see CONTRIBUTORS.rst                                           #
# Copyright © 2023 Sequana dev team                                       #
# See the COPYRIGHT file for details                                      #
#                                                                         #
# Versionix is free software: you can redistribute it and/or modify       #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# Versionix  is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program (COPYING file).                                 #
# If not, see <http://www.gnu.org/licenses/>.                             #
###########################################################################
""".. rubric:: Standalone application dedicated to Damona"""
import click
import sys


from versionix import version
from versionix.parser import get_version


__all__ = ["main"]

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command()
@click.argument("standalone", required=False, type=click.STRING, default=None)
@click.version_option(version)
@click.option("--stats", is_flag=True, help="Prints number of registered tools")
@click.option("--registered", is_flag=True, help="Prints the list of registered tools")
def main(**kwargs):
    """Versionix returns the version of installed software.

        versionix fastqc

    You can check the list of registered tools as follows

        versionix --registered


    """
    if kwargs["stats"]:
        from versionix.registry import metadata
        click.echo(f"There are currently {len(metadata.keys())} registered tools in Versionix") 
    elif kwargs["registered"]:
        from versionix.registry import metadata
        names = sorted(metadata.keys())
        for name in names:
            click.echo(f"{name}") 
    else:
        if kwargs["standalone"] is None:
            click.echo("No standalone was provided. You must provide one. You can use --registered to see the current list'")
            sys.exit(1)
        else:
            click.echo(get_version(kwargs["standalone"]))
