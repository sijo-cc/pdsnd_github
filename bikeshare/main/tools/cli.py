import click


from core.bikeshare import command as bike_share_interact_command


@click.command()
def bike_share_interactive():
    bike_share_interact_command()
