import os

config_dict = {
    "server": 'https://10ax.online.tableau.com',
    "token_name": os.environ.get('PAT_TOKEN_NAME',''),
    "token_secret": os.environ.get('PAT_TOKEN_SECRET',''),
    "content_url": os.environ.get('PAT_CONTENT_URL',''),
    "api_version": '3.21',
}
