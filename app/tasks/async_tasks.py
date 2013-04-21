from celery import task
from app.repo_tools import *
from app.models.repository import Repository


@task()
def update_repos():
    """Update all repos in the system"""
    # Clone the remote repo to the machine
    for repo in Repository.objects.all():
        update_repo(repo)


@task()
def update_repo(repo):
    """Takes an instance of a repository model,
    clones the repo to the machine, performs the
    required updates and pushes back to the origin"""
    try:
        clone = repo.get_repo()
        # Update the repo in the required way
        print "updating repo %s" % repo.short_name
        if repo.source_type == 'tar' or repo.source_type == 'zip':
            archive_to_repo(repo.source_url, clone, repo.source_type)
        elif repo.source_type == 'file':
            file_to_repo(repo.source_url, clone)
        elif repo.source_type == 'svn':
            update_svn_repo(clone)
        elif repo.source_type == 'git':
            return  # I DON'T THINK WE'RE DOING THIS BUT IN CASE
        # Send this back to the origin
        # For some reason the remotes in clone get lost
        print "pushing %s to %s" % (repo.short_name, repo.get_repo().remotes.origin.url)
        repo.get_repo().remotes.origin.push("master")
    except:
        print "something broke for %s :(" % repo.short_name
