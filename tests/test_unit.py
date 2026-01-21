from pathlib import Path
import pytest

from pulumi_autodoc.gemini import engineer_prompt
from pulumi_autodoc.pulumi import get_pulumi_stack_jsons
from pulumi_autodoc.utils import sync_s3_directory


def test_engineer_prompt_single_string():
    stack_json = '{"resources": [{"name": "bucket"}]}'
    result = engineer_prompt(stack_json)
    assert isinstance(result, str)
    assert "Summarize the following Pulumi stack JSON in Markdown format" in result
    assert stack_json in result


@pytest.fixture
def mock_boto3_client(monkeypatch):
    class MockS3:
        def get_paginator(self, _):
            class Paginator:
                def paginate(self, Bucket, Prefix):
                    return [
                        {
                            "Contents": [
                                {"Key": f"{Prefix}file1.txt"},
                                {"Key": f"{Prefix}subdir/file2.txt"},
                            ]
                        }
                    ]

            return Paginator()

        def download_file(self, Bucket, Key, Filename):
            Path(Filename).parent.mkdir(parents=True, exist_ok=True)
            Path(Filename).touch()

    monkeypatch.setattr("boto3.client", lambda service: MockS3())


def test_sync_s3_directory_downloads_files(tmp_path, mock_boto3_client):
    bucket = "test-bucket"
    prefix = "test-prefix/"
    local_dir = tmp_path / "download"

    sync_s3_directory(bucket, prefix, local_dir)

    assert (local_dir / "file1.txt").exists()
    assert (local_dir / "subdir" / "file2.txt").exists()


def test_find_json_files_in_stack(tmp_path):
    # Setup stack directory with nested json files
    stack_dir = tmp_path / "stack"
    (stack_dir / "a").mkdir(parents=True)
    (stack_dir / "b").mkdir(parents=True)
    file1 = stack_dir / "a" / "file1.json"
    file2 = stack_dir / "b" / "file2.json"
    file3 = stack_dir / "b" / "not_json.txt"
    file1.write_text("{}")
    file2.write_text("{}")
    file3.write_text("not json")

    results = get_pulumi_stack_jsons(stack_dir)

    # Should return relative paths from stack_dir
    expected = {Path("a/file1.json"), Path("b/file2.json")}
    assert set(results) == expected
