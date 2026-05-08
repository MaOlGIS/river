"""Helpers pro filesystem a dataset discovery.

Funkce jsou záměrně bez vazby na desktopové GIS API. Notebook je používá pro
rychlé nalezení processing groups a pravděpodobných vektorových vstupů; vlastní
ověření geometrie a schématu probíhá až po načtení přes GeoPandas.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class GroupFolder:
    """Folder reprezentující jednu processing group, například region."""

    name: str
    path: Path


def safe_name(name: str, max_len: int = 48) -> str:
    """Vrátí konzervativní ASCII name vhodný pro GIS outputs."""

    cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", name).strip("_")
    if not cleaned:
        cleaned = "obj"
    if cleaned[0].isdigit():
        cleaned = f"n_{cleaned}"
    return cleaned[:max_len]


def group_folders(root: str | os.PathLike[str]) -> list[GroupFolder]:
    """Vrátí přímé child directories jako processing groups."""

    root_path = Path(root)
    return [
        GroupFolder(path.name, path)
        for path in sorted(root_path.iterdir())
        if path.is_dir()
    ]


def vector_files(
    folder: str | os.PathLike[str],
    extensions: Sequence[str] = (".shp", ".gpkg", ".geojson"),
) -> list[Path]:
    """Vrátí pravděpodobné vector datasets v jednom folderu."""

    wanted = {ext.lower() for ext in extensions}
    return [
        path
        for path in sorted(Path(folder).iterdir())
        if path.is_file() and path.suffix.lower() in wanted
    ]


def keyword_score(path: str | os.PathLike[str], keywords: Iterable[str]) -> int:
    """Ohodnotí dataset name pomocí lower-case keyword hints."""

    name = Path(path).name.lower()
    return sum(1 for keyword in keywords if keyword.lower() in name)


def derive_region_code_from_name(name: str) -> str:
    """Extrahuje první dvoumístný code z folder nebo dataset name."""

    match = re.search(r"(?:^|[^0-9])(\d{2})(?:[^0-9]|$)", name)
    return match.group(1) if match else ""
