import click
from models import create_db, last_time_in_online, how_long_in_online
import os


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
    '--how_long', '-hl',  nargs=2, type=str,
    help='how long user in online. Time starts from START_DATE. Argument is limit, and uid'
)
@click.option(
    '--start_service', '-s',
    help='Start this service'
)
@click.option(
    '--test', '-t',
    help='testing this service'
)
def main(create, last_time, how_long, start_service, test):
    """
    Documentation
    """
    if create:
        create_db()
    if last_time:
        click.echo(last_time_in_online(last_time))
    if how_long:
        click.echo(how_long_in_online(how_long[0], how_long[1]))
    if start_service:
        os.system('source venv/bin/activate')
        os.system('python connection.py&')
        os.system('python app.py&')
    if test:
        os.system('python tests.py')


if __name__ == '__main__':
    main()