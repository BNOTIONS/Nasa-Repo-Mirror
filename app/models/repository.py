from app.models import Model
from django.db import models
from app.repo_tools import clone_repo


class Repository(Model):
    """Represents a repository to be reflected
    on GitHub."""
    GIT = 'git'
    SVN = 'svn'
    TAR = 'tar'
    ZIP = 'zip'
    FILE = 'file'
    SOURCE_TYPE_CHOICES = (
        (GIT, 'Git'),
        (SVN, 'Subversion'),
        (TAR, 'Tarball'),
        (ZIP, 'Zip Archive'),
        (FILE, 'Single File'),
    )
    name = models.CharField(max_length=64, blank=False)
    short_name = models.CharField(max_length=32, blank=False)
    remote_url = models.CharField(max_length=255, blank=False)
    source_url = models.CharField(max_length=255, blank=False)
    source_type = models.CharField(
        max_length=255, blank=False,
        choices=SOURCE_TYPE_CHOICES, default=SVN)

    def get_repo(self):
        return clone_repo(self.remote_url)
