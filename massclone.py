import os
import requests
import subprocess
import click

@click.command()
@click.option('--user', '-u', required=True, help='GitHub username')
@click.option('--exclude-non-github', is_flag=True, help='Exclude commits from non-GitHub users')
def main(user, exclude_non_github):
    """
    Main function to fetch and clone GitHub repositories for a given user.
    """
    # Create a temp directory for cloning repositories
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    os.chdir(temp_dir)

    click.echo("Fetching repositories...")
    repos = fetch_repositories(user)
    click.echo(f"Found {len(repos)} repositories.")
    clone_repositories(repos, exclude_non_github)

def fetch_repositories(user):
    """
    Fetch repositories for a given GitHub user.
    """
    api = f"https://api.github.com/users/{user}/repos"
    repos = []
    page = 1
    while True:
        response = requests.get(api, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            click.echo(f"Failed to fetch repositories: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def clone_repositories(repos, exclude_non_github):
    """
    Clone the list of repositories and create a text file with commit details.
    """
    for repo in repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        click.echo(f"Cloning {repo_name}...")
        subprocess.run(["git", "clone", clone_url])

        # Change directory to the cloned repository
        os.chdir(repo_name)

        # Fetch commit details
        click.echo(f"Fetching commits for {repo_name}...")
        commits = fetch_commits(repo["owner"]["login"], repo_name, exclude_non_github)

        # Write commits to a text file
        with open("commits.txt", "w") as f:
            for commit in commits:
                f.write(f"Author: {commit['author']}\n")
                f.write(f"Message: {commit['message']}\n")
                f.write(f"Date: {commit['date']}\n")
                f.write("-" * 40 + "\n")

        # Change back to the parent directory
        os.chdir("..")

def fetch_commits(owner, repo_name, exclude_non_github):
    """
    Fetch commits for a given repository.
    """
    api = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    commits = []
    page = 1
    while True:
        response = requests.get(api, params={"per_page": 100, "page": page})
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

