import click


@click.group()
def cli():
    click.echo("Welcome to Python Pomodoro.")


@cli.command("start")
def start():
    click.echo("Starting timer. (Not yet implemented)")

    # Check for arguments (to determin focus and break timer duration. Anything else???)
    # Check for config file
    # If no config file, create one
    #


@cli.command("pause")
def pause():
    click.echo("Pausing timer. (not yet implemented)")


@cli.command("resume")
def resume():
    click.echo("Resuming timer. (not yet implemented)")


@cli.command("cancel")
def cancel():
    click.echo("Canceling timer. (not yet implemented)")


@cli.command("status")
def status():
    click.echo("Getting timer status. (not yet implemented)")


# ----- Config Group -----
@cli.group("config")
def config():
    """Manage pmdro configuration"""
    click.echo("Setting config. (not yet implemented)")


@config.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing config file")
def init(force):
    """Create a new config file with defaults"""
    pass
