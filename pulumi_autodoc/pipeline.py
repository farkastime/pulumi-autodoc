import logging
from pathlib import Path

from pulumi import get_pulumi_stack_jsons
from gemini import get_gemini_summary, engineer_prompt
from utils import parse_s3_path, sync_s3_directory, combine_md_files


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline(config: dict):
    bucket, prefix = parse_s3_path(config["pulumi_stacks_s3_remote"])

    if not config["local_pulumi_dir"].exists() or config["overwrite_pulumi_dir"]:
        logger.info("Syncing Pulumi stack dir from S3...")
        sync_s3_directory(bucket, prefix, local_dir=config["local_pulumi_dir"])
    jsons = get_pulumi_stack_jsons(config["local_pulumi_dir"])
    for json in jsons:
        logger.info(f"Processing {json}")
        md_path = config["local_summary_dir"] / Path(json).with_suffix(".md")
        if md_path.exists() and not config["overwrite_summaries"]:
            logger.info(f"Markdown file {md_path} already exists. Skipping.")
            continue
        with open(config["local_pulumi_dir"] / json) as f:
            json_str = f.read()
            prompt = engineer_prompt(json_str)
            summary = get_gemini_summary(prompt, config["api_key"], config["endpoint"])
            md_path.parent.mkdir(parents=True, exist_ok=True)
            with open(md_path, "w") as f:
                f.write(f"# Pulumi Stack Summary\n\n{summary}\n")
    combine_md_files(
        config["local_summary_dir"],
        config["local_summary_dir"].parent / "combined_summary.md",
    )
