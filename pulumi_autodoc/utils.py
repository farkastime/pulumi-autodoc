import requests
from pathlib import Path
from typing import Tuple

import boto3


def get_gemini_summary(prompt, api_key, endpoint):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    summary = result["candidates"][0]["content"]["parts"][0]["text"]
    return summary


def engineer_prompt(stack_json) -> str:
    preamble = "Summarize the following Pulumi stack JSON in Markdown format"
    return f"{preamble}:\n\n{stack_json}\n\n"


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
