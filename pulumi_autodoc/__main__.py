from argparse import ArgumentParser
import os
from pathlib import Path

from pipeline import run_pipeline


def parse_args():
    parser = ArgumentParser(description="Run the scaling pipeline with a config file.")
    return parser.parse_args()


def parse_env() -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    endpoint = os.getenv("GEMINI_API_ENDPOINT")
    s3_remote = os.getenv("PULUMI_STACKS_S3_REMOTE")
    local_pulumi_dir = os.getenv("LOCAL_PULUMI_DIR", "data/.pulumi")
    local_summary_dir = os.getenv("LOCAL_SUMMARY_DIR", "data/output")
    overwrite_pulumi_dir = os.getenv("OVERWRITE_PULUMI_DIR", "false").lower() == "true"
    overwrite_summaries = os.getenv("OVERWRITE_SUMMARIES", "false").lower() == "true"
    return {
        "api_key": api_key,
        "endpoint": endpoint,
        "pulumi_stacks_s3_remote": s3_remote,
        "local_pulumi_dir": Path(local_pulumi_dir),
        "local_summary_dir": Path(local_summary_dir),
        "overwrite_pulumi_dir": overwrite_pulumi_dir,
        "overwrite_summaries": overwrite_summaries,
    }


def main(config: dict):
    run_pipeline(config=config)


if __name__ == "__main__":
    args = parse_args()
    config = parse_env()
    main(config=config)
