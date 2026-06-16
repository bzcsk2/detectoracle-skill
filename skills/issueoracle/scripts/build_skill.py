"""Build issueoracle.skill bundle (cross-platform)."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ROOT = SKILL_DIR.parent.parent
DIST = ROOT / "dist"
OUT = DIST / "issueoracle.skill"

EXCLUDES = {
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
}

REQUIRED_ENTRIES = [
    "SKILL.md",
    "scripts/issueoracle.py",
    "scripts/lib/schema.py",
    "packs/",
    "references/",
]


def should_include(path: Path) -> bool:
    parts = path.parts
    for exclude in EXCLUDES:
        if exclude.startswith("*") and exclude.endswith("*"):
            if path.suffix == exclude[1:-1]:
                return False
        elif exclude in parts:
            return False
    return True


def verify_required(zf: zipfile.ZipFile) -> list[str]:
    missing: list[str] = []
    names = set(zf.namelist())
    for entry in REQUIRED_ENTRIES:
        if entry.endswith("/"):
            if not any(n.startswith(entry) for n in names):
                missing.append(entry)
        elif entry not in names:
            missing.append(entry)
    return missing


def main() -> int:
    DIST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in SKILL_DIR.rglob("*"):
            if path.is_file() and should_include(path):
                zf.write(path, path.relative_to(SKILL_DIR))

    missing = verify_required(zf)
    if missing:
        print(f"ERROR: missing required entries: {missing}")
        OUT.unlink()
        return 1

    size = OUT.stat().st_size
    print(f"Built: {OUT} ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
