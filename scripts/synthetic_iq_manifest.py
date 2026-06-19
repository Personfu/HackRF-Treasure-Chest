#!/usr/bin/env python3
"""Build a manifest for synthetic RF/IQ sample files.

The manifest labels generated samples for training visualizers. It does not
capture, decode, or classify real-world transmissions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a synthetic sample manifest for HackRF lab assets.")
    parser.add_argument("sample_dir", type=Path)
    parser.add_argument("--out", type=Path, default=Path("synthetic-iq-manifest.json"))
    args = parser.parse_args()

    files = []
    for path in sorted(args.sample_dir.glob("**/*")):
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        files.append({
            "path": str(path.relative_to(args.sample_dir)),
            "bytes": path.stat().st_size,
            "sha256": digest,
            "source": "synthetic-generated",
            "allowedUse": "education, visualizer testing, receive-only RF literacy"
        })
    args.out.write_text(json.dumps({"samples": files}, indent=2), encoding="utf-8")
    print(f"wrote {args.out} with {len(files)} samples")


if __name__ == "__main__":
    main()
