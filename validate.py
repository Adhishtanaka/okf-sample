#!/usr/bin/env python3
"""Toy OKF consumer: parses a bundle, checks conformance, prints the knowledge graph."""

import sys
from pathlib import Path

from bundle_lib import load_bundle


def print_graph(root: Path, concepts: dict[str, dict]) -> None:
    print(f"Parsed {len(concepts)} concepts from {root}/\n")
    for key, meta in concepts.items():
        print(f"{key}  [{meta['type']}]")
        for link in meta["links"]:
            marker = "" if (root / link.lstrip("/")).exists() else "  (BROKEN)"
            print(f"  -> {link}{marker}")


def main() -> None:
    root = Path(__file__).parent / "bundle"
    concepts = load_bundle(root)
    print_graph(root, concepts)


def demo() -> None:
    """Self-check: a tiny in-memory bundle including one deliberately broken link."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.md").write_text(
            "---\ntype: Test\n---\nlinks to [b](/b.md) and [missing](/nope.md)\n"
        )
        (root / "b.md").write_text("---\ntype: Test\n---\nno links here\n")

        concepts = load_bundle(root)
        assert len(concepts) == 2
        assert concepts["/a.md"]["type"] == "Test"
        assert concepts["/a.md"]["links"] == ["/b.md", "/nope.md"]
        assert not (root / "nope.md").exists()  # confirms the broken-link case is real
    print("demo(): self-check passed")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        main()
