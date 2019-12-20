import click
from models import create_db, last_time_in_online, how_long_in_online


@click.command()
@click.option(
    '--create', '-c',
    help='Create database'
)
@click.option(
    '--last_time', '-lt',  nargs=1, type=str,
    help='When user was last time in online. Argument is vk_id or vk_uid'
)
@click.option(
    '--how_long', '-hl',  nargs=1, type=int,
    help='how long user in online. Time starts from START_DATE. Argument is limit'
)
def main(create, last_time, how_long):
    """
    Documentation
    """
    if create:
        create_db()
    if last_time:
        click.echo(last_time_in_online(last_time))
    if how_long:
        click.echo(how_long_in_online(how_long))


if __name__ == '__main__':
    main()