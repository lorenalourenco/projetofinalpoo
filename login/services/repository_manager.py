import os
import git
from login.models import Repository
class RepositoryManager:
    def __init__(self, user, repo_url):
        self.user = user
        self.repo_url = repo_url
        self.target_dir = os.path.join('repos', f'{user.username}_{repo_url.split("/")[-1]}')

    def repository_exists(self):
        return os.path.exists(self.target_dir)

    def clone_repository(self):
        if self.repository_exists():
            raise FileExistsError("O repositório já existe.")
        git.Repo.clone_from(self.repo_url, self.target_dir)

    def save_to_database(self):
        repo = Repository(user=self.user, repo_url=self.repo_url)
        repo.save()
        return repo
