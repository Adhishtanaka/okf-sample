"""Shared OKF bundle parsing, used by validate.py and mcp_server/server.py."""

import re
from pathlib import Path

import yaml

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s]+\.md)\)")


def parse_concept(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    _, frontmatter, body = text.split("---\n", 2)
    meta = yaml.safe_load(frontmatter) or {}
    if not meta.get("type"):
        raise ValueError(f"{path}: missing required 'type' field")
    meta["links"] = LINK_RE.findall(body)
    meta["body"] = body
    return meta


def load_bundle(root: Path) -> dict[str, dict]:
    concepts = {}
    for path in sorted(root.rglob("*.md")):
        if path.name in RESERVED:
            continue
        key = "/" + str(path.relative_to(root))
        concepts[key] = parse_concept(path)
    return concepts
