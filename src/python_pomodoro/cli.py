import click

from python_pomodoro.config import (
    CONFIG_SCHEMA,
    get_config_path,
    create_config_template,
    get_effective_config,
)


@click.group()
def cli():
    # click.echo("Welcome to Python Pomodoro.")
    pass


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
    pass


@config.command("init")
@click.option("--force", is_flag=True, help="Overwrite existing config file")
def init(force):
    """Create a new config file with defaults"""

    # Get config path.
    config_path = get_config_path()

    # Handle if file already exists and '--force' is not used.
    if config_path.exists() and not force:
        click.echo("Error: Config file already exists", err=True)
        click.echo(f"Location: {config_path}")
        click.echo(
            "Use '--force' option to overwite config to defaults, or edit file directly."
        )
        raise click.Abort()

    # Create contents of default config template.
    template_content = create_config_template()

    # Create parent directories if they don't already exist.
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        click.echo(f"Error: Failed to create parent directory: {e}", err=True)
        raise click.Abort()

    # Write config template contents to 'config_path'.
    try:
        config_path.write_text(template_content)
    except OSError as e:
        click.echo(
            f"Error: Failed to write default config to {config_path}: {e}", err=True
        )
        raise click.Abort()

    # Provide 'success' feedback.
    click.echo(f"Successfully initialized config file at '{config_path}'")


@config.command("show")
def show():
    """Display current effective configuration"""

    config_path = get_config_path()

    if config_path.exists():
        click.echo(f"Config file: {config_path}")
        click.echo("To edit: open this file in your preferred editor.")
    else:
        click.echo(f"Config file: {config_path} (not found, using defaults instead)")
        click.echo("To create config file: run the 'pmdro config init' command.")

    click.echo()

    effective_config = get_effective_config()

    click.echo("Current configuration:")
    for key, value in effective_config.items():
        comment = CONFIG_SCHEMA[key]["comment"]
        click.echo(f"  {key} = {value}  # {comment}")
