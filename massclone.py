import os
import requests
import subprocess
import click

@click.command()
@click.option('--token', '-t', help='Your GitHub API token')
@click.option('--user', '-u', required=True, help='GitHub username')
@click.option('--exclude-non-github', is_flag=True, help='Exclude commits from non-GitHub users')
@click.option('--allow-forks', is_flag=True, help='Allow cloning of forked repositories')
def main(user, token, exclude_non_github, allow_forks):
    """
    Main function to fetch and clone GitHub repositories for a given user.
    """
    # Create a temp directory for cloning repositories
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    os.chdir(temp_dir)

    click.echo("Fetching repositories...")
    repos = fetch_repositories(user, token)
    click.echo(f"Found {len(repos)} repositories.")
    clone_repositories(repos, exclude_non_github, token, allow_forks)

def fetch_repositories(user, token):
    """
    Fetch repositories for a given GitHub user.
    """
    headers = {}
    if token:
        headers = {"Authorization": f"token {token}"}

    api = f"https://api.github.com/users/{user}/repos"
    repos = []
    page = 1
    while True:
        response = requests.get(api, headers=headers, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            click.echo(f"Failed to fetch repositories: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def clone_repositories(repos, exclude_non_github, token, allow_forks):
    """
    Clone the list of repositories and fetch all branches.
    """
    for repo in repos:
        repo_name = repo["name"]

        # Skip forks if --allow-forks is not set
        if not allow_forks and repo.get("fork", False):
            click.echo(f"Skipping forked repository '{repo_name}'.")
            continue

        # Skip specific repositories like 'ghscraper' or 'DeepFaceLab'
        if repo_name == 'ghscraper' or repo_name == 'DeepFaceLab':
            click.echo(f"Skipping repository '{repo_name}' to avoid scraping itself.")
            continue

        clone_url = repo["clone_url"]
        click.echo(f"Cloning {repo_name}...")

        try:
            # Use --quiet to suppress prompts and --no-verify to disable hooks
            subprocess.run(["git", "clone", "--quiet", clone_url], check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Failed to clone repository '{repo_name}': {e}")
            continue

        # Change directory to the cloned repository
        try:
            os.chdir(repo_name)
        except FileNotFoundError:
            click.echo(f"Repository directory '{repo_name}' not found. Skipping...")
            continue

        # Fetch all branches
        click.echo(f"Fetching all branches for {repo_name}...")
        subprocess.run(["git", "fetch", "--all"], check=False)

        # Fetch commit details
        click.echo(f"Fetching commits for {repo_name}...")
        commits = fetch_commits(repo["owner"]["login"], repo_name, exclude_non_github, token)

        # Write commits to a text file
        with open("commits.txt", "w") as f:
            for commit in commits:
                f.write(f"Author: {commit['author']}\n")
                f.write(f"Message: {commit['message']}\n")
                f.write(f"Date: {commit['date']}\n")
                f.write("-" * 40 + "\n")

        # Change back to the parent directory
        os.chdir("..")

def fetch_commits(owner, repo_name, exclude_non_github, token):
    """
    Fetch commits for a given repository.
    """
    headers = {}
    if token:
        headers = {"Authorization": f"token {token}"}

    api = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    commits = []
    page = 1
    while True:
        response = requests.get(api, headers=headers, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            click.echo(f"Failed to fetch commits: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        for commit in data:
            author = commit["commit"]["author"]
            if exclude_non_github and commit["author"] is None:
                continue
            commits.append({
                "author": author["name"] if author else "Unknown",
                "message": commit["commit"]["message"],
                "date": author["date"] if author else "Unknown"
            })
        page += 1
    return commits

if __name__ == "__main__":
    main()

