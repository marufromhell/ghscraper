Has 2 scripts

The script that puts gitfive light and zen 6 feet under.
Ghscraper clones repos and logs commits, making commit indexes in every directory, aswell as a email list in the current directory(with --e flag). While there are better ways to do this than cloning, it doesnt cause rate limiting(as much) and allows you to search for api keys, passwords, emails, or other sensitive info.

# ghscraper.py
args:
- -t, your PAT token(not required unless cloning alot repos or encountering errors)
- -u, github target username
- --exclude-non-github, ignores git name in commit logs.
- --allow-forks, fork repos are auto removed, because they likely have no personal data and give many false email scrapes 
- --email-scrape, finds all emails used on PERSONAL repos and sorts by frequency(overpowered)
# grepr.sh (grep -r, but with 1 or more dictionary files) VERY SLOW
args:
- path, usually temp
- dictionary(s), usually names, password lists, api keys. ect

# INSTALL
`pip install ghscraper_maru` to install ghscraper  
`curl https://raw.githubusercontent.com/marufromhell/ghscraper/refs/heads/main/grepr.sh && mv ./grepr.sh ~/.local/bin/grepr && chmod u+x ~/.local/bin/grepr`  to install grepr.sh  
`curl curl https://raw.githubusercontent.com/marufromhell/ghscraper/refs/heads/main/names.txt` for basic name list  

# Name lists
The name lists are a way to check for name leaks.
If you are offensive, you would use a name list with many names on it, aswell as password lists, if you have the time.
if you are defensive, you would make a list with the following things:  
- Your name
- All of your api keys
- passwords
- Emails or any personal information that can lead to yourself.

# If you find yourself on this.
- if you were using a gmail at any point, check ghunt to see if you have a public google maps account, you probably do.
  
I would add the ability to clone most commits, but i dont have enough time or storage space for that. if i feel like it ill find a way to check the byte/file diff and have a set allowed change diff.

