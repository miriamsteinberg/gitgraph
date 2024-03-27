import git
import os


def get_repo(token):

    # Path to the directory where the repository is cloned
    repo_dir = 'clone'
    repo_url = f'https://{token}@github.com/CTFd/CTFd'

    # user_name = 'miriamsteinberg'
    # repo_url = f'https://{token}@github.com/{user_name}/CTFd'

    # Check if the .git directory exists in the specified path
    if os.path.isdir(os.path.join(repo_dir, '.git')):
        repo = git.Repo(repo_dir)
    else:
        repo = git.Repo.clone_from(repo_url, repo_dir)  # to first time

    return repo
