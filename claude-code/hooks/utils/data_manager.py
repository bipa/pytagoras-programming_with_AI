
import subprocess
import pathlib
import re
import sys
import json
import datetime
import os
import pwd


# ───────────── helpers ────────────────────────────────────────────────────── #
def repo_root() -> pathlib.Path:
    """Return the repository root via git."""
    return pathlib.Path(
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    )


def current_branch() -> str:
    """Return the current git branch name."""
    return subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()


def current_user() -> str:
    """Best‑effort grab of the username running the hook."""
    try:
        return os.getlogin()
    except OSError:
        return (
            os.getenv("USER")
            or pwd.getpwuid(os.getuid()).pw_name
            or "unknown"
        )
        
def repo_folder_name() -> str:
    """Return the name of the folder containing the repository."""
    return repo_root().name


def extract_feature_name(branch: str) -> str:
    """Extract the feature name from a branch name.
    
    Args:
        branch: The branch name, potentially in format 'XXXX_featurename'
    
    Returns:
        The feature name part (after underscore) or the original branch name if no underscore
    """
    if "_" in branch:
        return branch.split("_", 1)[1]
    return branch

def extract_feature_number(branch: str) -> str | None:
    """Extract the feature number from a branch name.
    
    Args:
        branch: The branch name, potentially in format 'XXXX_featurename'
    
    Returns:
        The feature number (before underscore) as string or None if no underscore/number
    """
    folder = find_feature_folder()
    if not folder:
        return None
    folder_name_parts = folder.name.split("_", 1)
    if len(folder_name_parts) < 1:
        return None
    number_part = folder_name_parts[0]
    return number_part if len(number_part) == 4 and number_part.isdigit() else None

def find_feature_folder() -> pathlib.Path | None:
    """Locate ./planning/features/XXXX_<branch> with the highest XXXX."""
    branch = current_branch()
    base = repo_root() / "planning" / "features"
    pattern = re.compile(rf"^(\d+)_({re.escape(branch)})$")
    matches: list[tuple[int, pathlib.Path]] = [
        (int(m.group(1)), d)
        for d in base.iterdir()
        if d.is_dir() and (m := pattern.match(d.name))
    ]
    if not matches:
        return None
    _, folder = max(matches, key=lambda t: t[0])
    return folder


def find_feature_log_path() -> pathlib.Path | None:
    """Locate ./planning/features/XXXX_<branch>/log.json with the highest XXXX."""
    folder = find_feature_folder()
    if not folder:
        return None
    return folder / "log.json"