from argparse import ArgumentParser
import os


def parse_args():
    parser = ArgumentParser(description="Run the scaling pipeline with a config file.")
    parser.add_argument("-R", "--remote", required=False, help="AWS S3 URI to stacks.")
    return parser.parse_args()


def parse_env() -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    endpoint = os.getenv("GEMINI_ENDPOINT")
    s3_remote = os.getenv("PULUMI_S3_REMOTE")
    return {"api_key": api_key, "endpoint": endpoint, "pulumi_s3_remote": s3_remote}


def main(config: dict):
    pass


if __name__ == "__main__":
    args = parse_args()
    config = parse_env()
    main(config=config)

