import logging
import requests


def extract(token, repo_url):
    logger = logging.getLogger()
    logger.info('Fetching data from GitHub...')
    logger.debug('check if debug disabled')

    latest_releases, forks_count, stargazers_count, contributors_count, pull_requests_count, sorted_contributors = (
        get_github_data(token, repo_url))

    logger.info(f'Latest 3 releases of CTFd: {latest_releases}')
    logger.info(f'Number of forks: {forks_count}')
    logger.info(f'Number of stars: {stargazers_count}')
    logger.info(f'Number of contributors: {contributors_count}')
    logger.info(f'Number of pull requests: {pull_requests_count}')

    logger.info('Descending order list of contributors per amount of pull requests:')
    for contributor, pulls in sorted_contributors:
        logger.info(f'{contributor}: {pulls} pull requests')


def get_github_data(token, repo_url):
    headers = {'Authorization': f'token {token}'}

    # Get latest 3 releases of CTFd
    releases_response = requests.get(f'{repo_url}/releases', headers=headers)
    latest_releases = [release['name'] for release in releases_response.json()[:3]]

    # Get number of forks, stars, contributors, pull requests
    repo_response = requests.get(repo_url, headers=headers)
    forks_count = repo_response.json()['forks_count']
    stargazers_count = repo_response.json()['stargazers_count']

    # Get contributors per amount of pull requests
    contributors_response = requests.get(f'{repo_url}/contributors', headers=headers)
    contributors_count = len(contributors_response.json())

    # Get contributors per amount of pull requests
    contributors_pulls = {}
    contributors_response = requests.get(f'{repo_url}/pulls', headers=headers)
    pull_requests_count = len(contributors_response.json())
    for pull in contributors_response.json():
        contributor = pull['user']['login']
        # Increment the pull request count for the contributor
        if contributor in contributors_pulls:
            contributors_pulls[contributor] += 1
        else:
            contributors_pulls[contributor] = 1

    sorted_contributors = sorted(contributors_pulls.items(), key=lambda x: x[1], reverse=True)

    return (latest_releases, forks_count, stargazers_count,
            contributors_count,
            pull_requests_count, sorted_contributors)
