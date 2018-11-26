# Automate github workflows

`$ pipenv install`
`$ pipenv run python server.py`

The service will periodically theck for pull requests and merge automatically if all conditions are met and the PR is in a `mergeable` state.

## Add a pull request
`curl -H "Content-Type: application/json" -X POST --data '{"url":"https://github.com/szaboat/test-repo/pull/1/"}' http://localhost:5000/add`
