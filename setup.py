from setuptools import setup, find_packages
from configparser import ConfigParser

version = "0.5.dev0"

long_description = "\n\n".join([open("README.md").read(), open("CHANGES.md").read()])

def parse_pipfile(development = False):
    """Reads package requirements from Pipfile."""
    cfg = ConfigParser()
    cfg.read('Pipfile')
    dev_packages = [p.strip('"') for p in cfg['dev-packages']]
    relevant_packages = [
        p.strip('"') for p in cfg['packages'] if "inspire-etf-validator" not in p
    ]
    if development:
        return dev_packages
    else:
        return relevant_packages


setup(
    name="inspire-etf-validator",
    version=version,
    description="Python wrapper that runs and aggregates the EU inspire ETF validator",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Programming Language :: Python :: 3"],
    keywords=["inspire-etf-validator"],
    author="William Loosman",
    author_email="william.loosman@kadaster.nl",
    url="https://github.com/PDOK/inspire-etf-validator",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_pipfile(),
    tests_require=parse_pipfile(True),
    entry_points={
        "console_scripts": [
            "etf = inspire_etf_validator.cli:inspire_etf_validator_command"
        ]
    },
)
