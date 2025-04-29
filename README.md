Has 2 scripts
# ghscraper.py
args:
- -t, your PAT token(not required unless cloning 50+ repos or encountering errors)
- -u, github target username
- --exclude-non-github, ignores git name in commit logs.
- --allow-forks, fork repos are auto removed, because they likely have no personal data and give many false email scrapes 
- --email-scrape, finds all emails used on PERSONAL repos and sorts by frequency(overpowered)
# grepr.sh
args:
- path, usually temp unless changed
- dictionary(s), usually names., password lists, api keys. ect

# INSTALL
`pip install ghscraper_marufromhell` to install ghscraper
`git clone https://github.com/marufromhell/grepr.git && cd grepr && sudo mv ./grepr /bin/grepr && chmod u+x /bin/grepr` to install grepr.sh

# Name lists
The name lists are a way to check for name leaks.
If you are offensive, you would use a name list with many names on it.  
if you are defensive, you would make a list with the following things:  
- Your name
- All of your api keys
- passwords
- Emails or any personal information that can lead to yourself.

# If you find yourself on this.
- if you were using a gmail at any point, check ghunt to see if you have a public google maps account, you probably do.
- If your email has your real name, delete your account
- if a repo has your real name, or any other thing in a dictionary attack, `git clone YOUR_REPO`, `rm -rf ./git`, delete the repo, remake the repo.
- This should be a reminder that you should use a non google email, and never use your real name online.


I would add the ability to clone most commits, but i dont have enough time or storage space for that. if i feel like it ill find a way to check the byte/file diff and have a set allowed change diff.

