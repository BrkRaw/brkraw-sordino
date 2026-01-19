#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import json
from pathlib import Path


def main() -> int:
    event_name = os.environ.get("EVENT_NAME", "")
    input_tag = os.environ.get("INPUT_TAG", "")
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        raise SystemExit("GITHUB_OUTPUT not set")

    if event_name == "workflow_dispatch" and input_tag:
        tag = input_tag
    else:
        metadata_path = Path("release_metadata.json")
        if event_name == "workflow_run" and not metadata_path.exists():
            with open(output_path, "a", encoding="utf-8") as handle:
                handle.write("tag=\n")
                handle.write("prerelease=true\n")
            return 0
        if not metadata_path.exists():
            raise SystemExit("release_metadata.json not found")
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        tag = data.get("tag", "")

    if not tag:
        raise SystemExit("Tag not resolved")

    prerelease = "true" if re.search(r"(a|b|rc)[0-9]*$", tag) else "false"
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"tag={tag}\n")
        handle.write(f"prerelease={prerelease}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
