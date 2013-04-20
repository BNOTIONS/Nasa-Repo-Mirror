from tempfile import SpooledTemporaryFile
import requests
import tarfile
import zipfile


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
    # Extract to the repo path
    archive.extractall(repo.working_dir)
    # Add and commit everything!
    repo.git.add(".", A=True)
    repo.git.commit(m="New archive version")
    # Cleanup, outta here!
    archive.close()
    tmp.close()
