import yaml
from pathlib import Path
from typing import List, Optional, Any, Dict

config = yaml.safe_load(open("mkdocs.yml", "r"))

order = [
    'Programming',
    'LaTeX',
    'Ubuntu',
    'Windows'
]

base_path = Path("manuals")


def add_item(nav: List, item: Path):
    if item.is_dir():
        nav.append({item.name: []})
        process_dir(nav[-1][item.name], item)
    else:
        nav.append({item.with_suffix('').name: item.relative_to(base_path).as_posix()})


def process_dir(nav: List, path: Path, order: Optional[List[str]] = None):
    # first process the ordered items
    if order is not None:
        for item in order:
            item_path = path / item
            add_item(nav, item_path)

    # then process directories
    for item in path.glob("*/"):
        if item.is_dir():
            if not order or item.name not in order:
                add_item(nav, item)

    # then process the rest
    for item in path.glob("*"):
        if item.is_file() and item.suffix == ".md":
            add_item(nav, item)


nav = []
process_dir(nav, Path("manuals"), order)
config["nav"] = nav

if config:
    yaml.safe_dump(config, open("mkdocs.yml", "w"))