import mimetypes
import pathlib

import click
import filetype
import magic
import puremagic

from click import secho


@click.group()
def cli():
    pass


@cli.command()
@click.option("--file", help="path to file")
def single(file):
    kind = filetype.guess(file)
    if kind is None:
        click.secho("filetype failed", fg="red")
    print(f"File extensions: {kind.extension}")
    print(f"File MIME type: {kind.mime}")

    type: str = magic.from_file(file, mime=True)
    if type.split("/")[0] != "audio":
        click.secho("python magic mime type doesn't match", fg="red")
    print(f"python magic mime: {type}")

    mime = mimetypes.guess_type(file, strict=True)
    if not mime:
        click.secho("mimetypes couldn't guess the type", fg="red")
    print(f"mimtypes: {mime}")

    pure = puremagic.magic_file(file)
    print(pure)
    if pure[0].mime_type.split("/")[0] != "audio":
        click.secho("puremagic didn't guess the file as audio", fg="red")


@cli.command()
@click.option("--dir", help="path to dir holding files")
def batch(dir):
    error_list = []

    pathlist = pathlib.Path(dir).rglob("*.*")
    for path in pathlist:
        str_path = str(path.absolute())
        secho("\n\n")
        secho(str_path, fg="bright_white")
        secho("\n")
        click.secho("filetypes", fg="yellow")
        kind = filetype.guess(str_path)
        if kind is None:
            error_list.append(("filetypes", str_path))
        click.secho(f"File extensions: {kind.extension}", fg="yellow")
        click.secho(f"File MIME type: {kind.mime}", fg="yellow")

        secho("magic", fg="cyan")
        type: str = magic.from_file(str_path, mime=True)
        if type.split("/")[0] != "audio":
            error_list.append(("magic", str_path))
        secho(f"python magic mime: {type}", fg="cyan")

        secho("pure", fg="magenta")
        pure = puremagic.magic_file(str_path)
        secho(pure, fg="magenta")
        if pure[0].mime_type.split("/")[0] != "audio" or pure[0].confidence < 0.5:
            error_list.append(("pure", str_path))

        secho("mimetypes", fg="blue")
        mime = mimetypes.guess_type(str_path, strict=True)
        if not mime:
            error_list.append(("mimetypes", str_path))
        secho(f"mimtypes: {mime}", fg="blue")

    for err in error_list:
        click.secho(f"{err[0]} found {err[1]} problematic", fg="red")

    if not error_list:
        click.secho("no errors", fg="green")


if __name__ == "__main__":
    cli()
