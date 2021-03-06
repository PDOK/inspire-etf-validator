# inspire-etf-validator
Python script to run Inspire ETF validation for every PDOK Inspire endpoint in NGR.

## Installation

We can be installed with:

```bash
pip3 install inspire-etf-validator
```

## Usage

Execute the script like this:

`inspire_etf_validator -r /home/pdok/test`

Or use pipenv:

`pipenv run inspire_etf_validator -r /home/pdok/test`

Options:

* `-r` or `--result_path` -> Path pointing to a directory used for the output -> default: `../`;
* `-e` or `--inspire_etf_endpoint` -> URL of the Inspire ETF service used to validate -> default: `http://localhost:8080/validator`; 
* `-c` or `--enable-caching` -> Enables cache for retrieving NGR inspire endpoints.
* `-d` or `--debug-mode` -> Enables debug mode which will run tests for the first three endpoints.

## Development installation of this project itself

We're installed with [pipenv](https://docs.pipenv.org/), a handy wrapper
around pip and virtualenv. Install that first with `pip3 install pipenv`. Then run:

```bash
PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.8 --dev
```

In case you do not have python 3.8 on your machine, install python using 
[pyenv](https://github.com/pyenv/pyenv) and try the previous command again.
See install pyenv below for instructions. 

There will be a script you can run like this::

```bash
pipenv run inspire-etf-validator
```

It runs the `main()` function in `inspire-etf-validator/core.py`,
adjust that if necessary. The script is configured in `setup.py` (see
`entry_points`).

In order to get nicely formatted python files without having to spend manual
work on it, run the following command periodically:

```bash
pipenv run black inspire_etf_validator
```

Run the tests regularly. This also checks with pyflakes, black and it reports
coverage. Pure luxury:

```bash
pipenv run pytest
```

If you need a new dependency (like `requests`), add it in `setup.py` in
`install_requires`. Afterwards, run install again to actually install your
dependency:

```bash
pipenv install --dev
```

## Releasing 
Pipenv installs zest.releaser which allows you to release the package to a git(hub) repo. It has a 
`fullrelease` command that asks you a few questions, which you all respond to with `<enter>`:

```bash
pipenv run fullrelease
```
# Install pyenv
We can install pyenv by running the following commands: 

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
```

Also make sure to put pyenv in your `.bashrc` or `.zshrc` as instructed by the previous commands.
