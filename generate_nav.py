import yaml
from pathlib import Path

config = yaml.safe_load(open("mkdocs.yml", "r"))

order = [
    'Programming',
    'LaTeX',
    'Ubuntu',
    'Windows'
]

def add_item(nav: List)

def process_level(nav, path: Path, order: List[str]):
    #

nav