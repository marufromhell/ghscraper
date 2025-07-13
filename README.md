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
`pip install ghscraper_maru` in venv  
`git clone https://github.com/marufromhell/grepr.git && cd grepr && sudo mv ./grepr /bin/grepr && chmod u+x /bin/grepr`
