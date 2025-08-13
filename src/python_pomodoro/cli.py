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
def stop():
    click.echo("Canceling timer. (not yet implemented)")


@cli.command("status")
def status():
    click.echo("Getting timer status. (not yet implemented)")


@cli.command("config")
def config():
    click.echo("Setting config. (not yet implemented)")
