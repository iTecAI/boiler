import os
import rich_click as click
from rich.console import Console
from lib import *


@click.group(invoke_without_command=True)
@click.option("--git", default=None, help="Provide a git repository as the template source.")
@click.option("--path", default=None, type=click.Path(exists=True, file_okay=False, dir_okay=True), help="Provide an existing folder as the template source.")
@click.pass_context
def main(ctx: click.Context, git: str = None, path: str = None):
    console = Console()
    if not git and not path:
        console.print("[red]A source (git/path) must be provided.")
        exit(1)

    if git and path:
        console.print("[red]Only one template source is allowed.")
        exit(2)

    environment = BoilerEnvironment()

    if git:
        source = GitSource(git, environment.directory.name)
    else:
        source = PathSource(os.path.abspath(path), environment.directory.name)

    ctx.obj = ctx.with_resource(Accumulator(environment, source, console))


if __name__ == "__main__":
    main()
