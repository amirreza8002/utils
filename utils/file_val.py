import mimetypes
import pathlib

import click
import filetype
import magic
import puremagic
from click import secho

FILE_TYPES = [
    "application",
    "audio",
    "image",
    "video",
]


def check_filetype(file: str, kind: str, verbose=True):
    secho("python-filetype", fg="yellow")
    types = filetype.guess(file)
    secho(f"File extensions: {types.extension}", fg="yellow")
    secho(f"File MIME type: {types.mime}", fg="yellow")
    if types is None or types.mime.split("/")[0] != kind:
        if verbose:
            click.secho("filetype failed", fg="red")
        return False
    return True


def check_magic(file: str, kind: str, verbose=True):
    secho("python-magic", fg="cyan")
    type: str = magic.from_file(file, mime=True)
    secho(f"python magic mime: {type}", fg="cyan")
    if type.split("/")[0] != kind:
        if verbose:
            click.secho("python magic mime type doesn't match", fg="red")
        return False
    return True


def check_mimetypes(file: str, kind: str, verbose=True):
    secho("mimetypes", fg="blue")
    mime = mimetypes.guess_type(file, strict=True)
    secho(f"mimtypes: {mime}", fg="blue")
    if not mime:
        if verbose:
            click.secho("mimetypes couldn't guess the type", fg="red")
    elif mime[0].split("/")[0] != kind:
        if verbose:
            secho("mimetypes found the wrong mime", fg="red")
    else:
        return True
    return False


def check_puremagic(file: str, kind: str, verbose=True):
    secho("puremagic", fg="magenta")
    pure = puremagic.magic_file(file)
    secho(pure, fg="magenta")
    if pure[0].mime_type.split("/")[0] != "audio" or pure[0].confidence < 0.5:
        if verbose:
            click.secho("puremagic didn't guess the file as audio", fg="red")
        return False
    return True


@click.group()
def cli():
    pass


@cli.command()
@click.option("--file", help="path to file")
@click.option(
    "--type",
    type=click.Choice(FILE_TYPES, case_sensitive=False),
    help="type of the file to validate",
    default="audio",
)
def single(file, type):
    check_filetype(file, type)

    check_magic(file, type)

    check_mimetypes(file, type)

    check_puremagic(file, type)


@cli.command()
@click.option("--dir", help="path to dir holding files", required=True)
@click.option(
    "--type",
    type=click.Choice(FILE_TYPES, case_sensitive=False),
    help="type of the file to validate",
    default="audio",
)
def batch(dir, type):
    error_list = []

    pathlist = pathlib.Path(dir).rglob("*.*")
    for path in pathlist:
        str_path = str(path.absolute())
        secho("\n\n")
        secho(str_path, fg="bright_white")
        secho("\n")

        types = check_filetype(str_path, type, verbose=False)
        if not types:
            error_list.append(("filetypes", str_path))

        pymagic = check_magic(str_path, type, False)
        if not pymagic:
            error_list.append(("magic", str_path))

        pure = check_puremagic(str_path, type, False)
        if not pure:
            error_list.append(("pure", str_path))

        mime = check_mimetypes(str_path, type, False)
        if not mime:
            error_list.append(("mimetypes", str_path))

    for err in error_list:
        click.secho(f"{err[0]} found {err[1]} problematic", fg="red")

    if not error_list:
        click.secho("no errors", fg="green")
