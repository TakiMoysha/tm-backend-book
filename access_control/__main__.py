import typer

from registry.commands import cli as registry_cli 

cli = typer.Typer(
    name="Access Control Manager",
    add_completion=True,
    pretty_exceptions_enable=False,
)

cli.add_typer(registry_cli, name="registry")
