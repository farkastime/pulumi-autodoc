from pathlib import Path
from typing import Tuple

import boto3


def parse_s3_path(s3_path: str) -> Tuple[str, str]:
    s3_path = s3_path.replace("s3://", "", 1)
    parts = s3_path.split("/", 1)
    bucket = parts[0]
    prefix = parts[1] if len(parts) > 1 else ""
    return bucket, prefix


def sync_s3_directory(bucket, prefix, local_dir):
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    local_dir = Path(local_dir)
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            s3_key = obj["Key"]
            rel_path = Path(s3_key).relative_to(prefix)
            local_path = local_dir / rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(bucket, s3_key, str(local_path))


def combine_md_files(root_dir, output_file):
    root = Path(root_dir)
    with open(output_file, "w", encoding="utf-8") as outfile:
        for md_file in sorted(root.rglob("*.md")):
            with open(md_file, "r", encoding="utf-8") as infile:
                outfile.write(f"# {md_file.relative_to(root)}\n\n")
                outfile.write(infile.read())
                outfile.write("\n\n")
