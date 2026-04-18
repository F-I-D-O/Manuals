import yaml
from pathlib import Path
from typing import List, Optional, Any, Dict

try:
    import pathspec
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "pathspec is required (install with mkdocs or: pip install pathspec)"
    ) from e

config = yaml.safe_load(open("mkdocs.yml", "r"))

order = [
    'Programming',
    'LaTeX',
    'Linux',
    'Windows'
]

base_path = Path("manuals")


def parse_exclude_patterns(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [line.strip() for line in raw.splitlines() if line.strip()]
    if isinstance(raw, list):
        return [str(p).strip() for p in raw if str(p).strip()]
    s = str(raw).strip()
    return [s] if s else []


def build_exclude_spec(config_dict: Dict[str, Any]) -> Optional[pathspec.PathSpec]:
    patterns = parse_exclude_patterns(config_dict.get("exclude_docs"))
    if not patterns:
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


exclude_spec = build_exclude_spec(config)


def is_doc_excluded(path: Path) -> bool:
    if exclude_spec is None:
        return False
    rel = path.relative_to(base_path)
    return exclude_spec.match_file(rel.as_posix())


def add_item(nav: List, item: Path):
    if item.is_dir():
        nav.append({item.name: []})
        process_dir(nav[-1][item.name], item)
    else:
        if item.suffix == ".md" and is_doc_excluded(item):
            return
        nav.append({item.with_suffix('').name: item.relative_to(base_path).as_posix()})


def process_dir(nav: List, path: Path, order: Optional[List[str]] = None):
    # first process the ordered items
    if order is not None:
        for item in order:
            item_path = path / item
            if item_path.is_file() and item_path.suffix == ".md" and is_doc_excluded(item_path):
                continue
            add_item(nav, item_path)

    # then process directories
    for item in path.glob("*/"):
        if item.is_dir():
            if not order or item.name not in order:
                add_item(nav, item)

    # then process the rest
    for item in path.glob("*"):
        if item.is_file() and item.suffix == ".md":
            if is_doc_excluded(item):
                continue
            add_item(nav, item)


nav = []
process_dir(nav, Path("manuals"), order)
config["nav"] = nav

if config:
    yaml.safe_dump(config, open("mkdocs.yml", "w"))
