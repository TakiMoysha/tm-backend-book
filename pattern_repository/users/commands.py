import typer



cli = typer.Typer(
    name="The Users Manager",
    help="Manage users",
    add_completion=True,
)

@cli.command(help="Show active users")
def list() -> None:
    typer.echo("Listing users...")
