from pathlib import Path

import click

from kks.ejudge import ejudge_submit
from kks.util import get_valid_session, load_links, prompt_choice, find_workspace


def get_problem_id():
    cwd = Path.cwd().resolve()
    workspace = find_workspace(cwd)
    if workspace is None:
        return None
    if len(cwd.parents) < 2 or cwd.parents[1] != workspace:
        return None
    return f'{cwd.parent.name}-{cwd.name}'


def find_solution():
    cwd = Path.cwd().resolve()
    c_files = list(cwd.glob('*.c'))
    if len(c_files) == 0:
        click.secho('No .c files found', fg='red', err=True)
        return None
    if len(c_files) > 1:
        click.secho('Multiple .c files found, use one as an argument', fg='red', err=True)
        return None
    return c_files[0]



@click.command(short_help='Submit a solutions')
@click.argument('file', type=click.Path(exists=True), required=False)
@click.option('-p', '--problem', type=str,
              help='manually specify the problem ID')
def submit(file, problem):
    """
    Submit a solution

    You should run this command from a synced directory or use -p option
    """

    if problem is None:
        problem = get_problem_id()
    if problem is None:
        click.secho('Could not detect the problem id, use -p option', fg='red')
        return

    if file is None:
        file = find_solution()
    if file is None:
        return

    session = get_valid_session()
    if session is None:
        return

    links = load_links()
    if links is None:
        click.secho('Auth data is invalid, use "kks auth" to authorize', fg='red', err=True)
        return

    def lang_choice(langs):
        choices = [e[0] for e in langs]
        lang_id = prompt_choice('Select a language / compiler', choices)
        return langs[lang_id]

    res, msg = ejudge_submit(links, session, file, problem, lang_choice)
    color = 'green' if res else 'red'
    click.secho(msg, fg=color)