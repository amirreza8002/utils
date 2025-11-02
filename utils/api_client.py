import json

import click

import httpx

import msgspec


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--format",
    help="json|msgpack|yaml|toml",
    prompt="data format (json|msgpack)",
    type=click.Choice(["json", "msgpack"], case_sensitive=False),
    default="json",
)
@click.option("--protocol", default="http", prompt="protocol")
@click.option("--domain", default="localhost", prompt="domain name")
@click.option("--port", default="8000", prompt="port")
@click.option(
    "--url", default="api", prompt="the url after domain and before rest version"
)
@click.option(
    "--version",
    help="rest version (v1, v2, ...), enter only the number",
    default="1",
    prompt="rest version",
)
@click.option("--endpoint", required=True, prompt="endpoint (after version)")
@click.option("--id", default="", prompt="detail object id (after endpoint)")
def get(format, protocol, domain, port, url, version, endpoint, id):
    format = (
        msgspec.msgpack
        if format == "msgpack"
        else msgspec.json
        if format == "json"
        else msgspec.toml
        if format == "toml"
        else msgspec.yaml
    )
    with httpx.Client() as client:
        data = client.get(
            f"{protocol}://{domain}{':' if port else ''}{port if port else ''}/{url}/v{
                version
            }/{endpoint}/{id}"
        )
    print("\n\n")
    print(json.dumps(format.decode(data.content), indent=4, sort_keys=True))
