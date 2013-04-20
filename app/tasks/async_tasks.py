from celery import task
from app.repo_tools import *


@task()
def add_task(x, y):
    return x + y


@task()
def update_repo(repo):
    """Takes an instance of a repository model,
    clones the repo to the machine, performs the
    required updates and pushes back to the origin"""
    # Clone the remote repo to the machine
    clone = repo.get_repo()
    # Update the repo in the required way
    if repo.source_type == 'tar' or source_type == 'zip':
        archive_to_repo(repo.source_url, clone, repo.source_type)
    elif repo.source_type == 'file':
        file_to_repo(repo.source_url, clone)
    elif repo.source_type == 'svn':
        pass  # FIGURE THIS OUT!!!
    elif repo.source_type == 'git':
        pass  # I DON'T THINK WE'RE DOING THIS BUT IN CASE
    # Send this back to the origin
    clone.remotes.origin.push()
