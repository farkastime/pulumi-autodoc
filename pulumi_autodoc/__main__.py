from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="Run the scaling pipeline with a config file.")
    parser.add_argument("-R", "--remote", required=True, help="AWS S3 URI to stacks.")
    return parser.parse_args()


def main(s3_remote: str):
    pass


if __name__ == "__main__":
    args = parse_args()
    main(s3_remote=args.remote)

