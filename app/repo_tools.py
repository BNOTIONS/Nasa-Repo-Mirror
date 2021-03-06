from tempfile import mkdtemp, SpooledTemporaryFile
from git import *
import os
import shutil
from os.path import basename
import requests
import tarfile
import zipfile


def clone_repo(remote_url):
    """Create a temporary instance of a repo based
    on the remote url. I don't think we can rely on
    persistent storage on heroku so we'll clone
    for each usage! Really small function but just in
    case we need some more boilerplate in the future"""
    return Repo.clone_from(remote_url, mkdtemp())


def update_svn_repo(repo):
    """Instruct a repo with a svn remote to update itself,
    and rebase the changes back into the repo"""
    repo.git.svn("fetch")
    repo.git.svn("rebase")


def archive_to_repo(archive_path, repo, archive_type="tar"):
    """Downloads a archive from the specified path,
    extracts it into the repo's directory, commits
    any changes from the previous version and pushes it
    to github!!!!"""
    # Download the tarball and stick it in a tempfile
    r = requests.get(archive_path)
    tmp = SpooledTemporaryFile()
    tmp.write(r.content)
    tmp.seek(0)
    # Open the tempfile contents as an actual tarball
    if archive_type == "tar":
        archive = tarfile.open(fileobj=tmp)
    elif archive_type == "zip":
        archive = zipfile.open(tmp)
    else:
        raise ValueError("Unrecognized Archive Type")
    # Clear working files
    clear_working_dir(repo.working_dir)
    # Extract to the repo path
    archive.extract(repo.working_dir)
    # Add and commit everything!
    try:
        repo.git.add(".", A=True)
        repo.git.commit(m="New archive version")
    except:
        pass  # May be that there was nothing new to commit
    # Cleanup, outta here!
    archive.close()
    tmp.close()


def file_to_repo(file_path, file_name, repo):
    """Downloads a file and sticks it into a repo.
    Adds and commits it. Currently we're using this for
    the single jar repo!!"""
    # Download the file and stick it in the directory!
    file_name = basename(file_path)
    r = requests.get(file_path)
    dest = "%s/%s" % (repo.working_dir, file_name)
    f = open(dest, "w")
    f.write(r.content)
    # Add and commit the file
    repo.git.add(dest)
    repo.git.commit(m="Added %s" % file_name)
    # Cleanup
    f.close()


def clear_working_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if ".git" not in os.path.join(root, f):
                os.unlink(os.path.join(root, f))
        for d in dirs:
            if ".git" not in os.path.join(root, d):
                shutil.rmtree(os.path.join(root, d))
