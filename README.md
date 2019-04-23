### Web Template

#### Installation Steps:
1. Run `sudo pip3 install pipenv`
2. Run `pipenv install` to install all dependencies.
3. Create `.env` from `.env_default`


#### Coding Instructions
1. For Adding Variable in Settings, Read from `.env` file. Always make sure `.env` and `.env_default` 
to remain in sync.

2. Make sure variable name in `settings.py` and `.env` file should be same. 
Naming Convension of variable should always be in Upper Case.

3. For Reading variable from `settings.py`, Follow: 
`from django.conf import settings` then `settings.VAR_NAME`


