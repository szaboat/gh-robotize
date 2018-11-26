import github3
import os

try:
    # Python 2
    prompt = raw_input
except NameError:
    # Python 3
    prompt = input

token = os.environ['GH_TOKEN']

g = github3.login(token=token)

def check_pr(pr_url):
    _, _, _, user, repo, _, id, _ = pr_url.split('/')
    pr = g.pull_request(user, repo, id)
    return pr
