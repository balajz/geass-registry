from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

from registrar.models.package import Kind, PackageType, Repository
from registrar.registry.registry import Registry

app = typer.Typer(help="Registrar CLI for managing the template registry.")
package_app = typer.Typer(help="Manage packages in the registry.")
repo_app = typer.Typer(help="Manage repositories within packages.")

app.add_typer(package_app, name="package")
app.add_typer(repo_app, name="repository")

# Default registry root is the parent directory of this file's grand-parent (i.e. g-registry)
DEFAULT_REGISTRY_ROOT = Path.cwd()


def get_registry(ctx: typer.Context) -> Registry:
    root = ctx.obj.get("root", DEFAULT_REGISTRY_ROOT)
    return Registry(str(root))


@app.callback()
def main(
    ctx: typer.Context,
    root: Annotated[
        Optional[Path], typer.Option(help="Path to the registry root directory.")
    ] = None,
):
    """
    Global options for Registrar.
    """
    ctx.ensure_object(dict)
    if root:
        ctx.obj["root"] = root


@package_app.command("init")
def init_package(
    ctx: typer.Context,
    id: Annotated[str, typer.Argument(help="The unique ID for the package.")],
    name: Annotated[
        str, typer.Option("--name", "-n", help="The display name of the package.")
    ],
    language: Annotated[
        str, typer.Option("--language", "-l", help="The primary programming language.")
    ],
    type: Annotated[
        PackageType, typer.Option("--type", "-t", help="The type of the package.")
    ] = PackageType.unknown,
    aliases: Annotated[
        Optional[List[str]],
        typer.Option("--alias", "-a", help="Aliases for the package."),
    ] = None,
    tags: Annotated[
        Optional[List[str]], typer.Option("--tag", help="Tags describing the package.")
    ] = None,
):
    """
    Initialize a new package in the registry.
    """
    registry = get_registry(ctx)

    # Check if it already exists
    pkg_idx = registry.index.get_package(id)
    if pkg_idx:
        typer.secho(
            f"Package '{id}' already exists in language '{pkg_idx.language}'.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)

    pkg = registry.add_package(
        id=id,
        name=name,
        language=language,
        type=type,
        aliases=aliases or [],
        tags=tags or [],
    )
    registry.flush_index()
    typer.secho(
        f"Successfully initialized package '{name}' under '{language}'.",
        fg=typer.colors.GREEN,
    )


@repo_app.command("add")
def add_repository(
    ctx: typer.Context,
    package_name: Annotated[
        str, typer.Argument(help="The name of the package to add the repository to.")
    ],
    owner: Annotated[
        str,
        typer.Option(
            "--owner", "-o", help="The GitHub repository owner (e.g., 'fastapi')."
        ),
    ],
    repo: Annotated[
        str, typer.Option("--repo", "-r", help="The GitHub repository name.")
    ],
    kind: Annotated[
        Kind, typer.Option("--kind", "-k", help="The kind of repository.")
    ] = Kind.unknown,
    stack: Annotated[
        Optional[List[str]],
        typer.Option("--stack", "-s", help="Technology stack used."),
    ] = None,
    tags: Annotated[
        Optional[List[str]],
        typer.Option("--tag", "-t", help="Tags for this repository."),
    ] = None,
    official: Annotated[
        bool,
        typer.Option("--official/--unofficial", help="Is this an official repository?"),
    ] = False,
    stars: Annotated[
        int, typer.Option("--stars", help="GitHub stars for the repository.")
    ] = 0,
    notes: Annotated[str, typer.Option("--notes", help="Any additional notes.")] = "",
):
    """
    Register a new repository under an existing package.
    """
    registry = get_registry(ctx)

    try:
        new_repo = Repository(
            owner=owner,
            repo=repo,
            kind=kind,
            stack=stack or [],
            tags=tags or [],
            official=official,
            stars=stars,
            notes=notes,
        )
        registry.add_repository(package_name, new_repo)

        # Flush index just in case, though adding a repo doesn't change index
        registry.flush_index()
        typer.secho(
            f"Successfully added repository '{owner}/{repo}' to package '{package_name}'.",
            fg=typer.colors.GREEN,
        )

    except ValueError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)
    except FileNotFoundError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
