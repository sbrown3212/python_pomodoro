import click


@click.group()
def cli():
    click.echo("Welcome to Python Pomodoro.")


@cli.command("start")
def start():
    click.echo("Starting timer. (Not yet implemented)")
