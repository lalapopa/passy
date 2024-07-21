# PASSY

<p align="center">
  <img src="https://www.yeoandyeo.com/wp-content/uploads/07_02_21_1253437873_AAB_560x292.jpg" />
</p>

# Installation

1. `git clone https://github.com/lalapopa/passy && cd ./passy`
1. `pip3 install -r requirements.txt`
1. `pyinstaller --add-data "./src/words_alpha.txt:." --onefile ./src/passy.py`
1. `cp ./dist/passy ~/.local/bin`
```
passy -h
usage: passy [-h] [-g] [-a]

optional arguments:
  -h, --help          show this help message and exit
  -g, --get_password  Get password
  -a, --add_password  Add password
```

# First setup

When run `passy -a` in first time. U need to setup you master password. And that
will create `~/passy` directory in home folder. 

```
All your password will be in '/home/lalapopa/passy'
Input new master password: 123
Rewrite it again: 123
[goes -a scenario from section "CLI Interaction example"]
```

# CLI interaction example 

[-a]    add password for some site or application 

```
$ passy -a
For what site or application: google.com
Username: john@outlook.com
Password: [if you wanna generate just press ENTER]
Rewrite same password: [if you wanna generate just press ENTER]
Note: work mail
Masterpassword is required: 123
Key written in main.vault
```

[-g]    get password
```
$ passy -g 
Masterpassword is required: 123
What pass do u need? 
1 - DuunoSite.com 
2 - Github
3 - shittypass.com
4 - google.com
Choose app:4 
Login: john@outlook.com
Can I show pass? (y/n) [automatically copy to clipboard if you type `n`]
Note: work mail 
```

P.S **don't** use 123 password

