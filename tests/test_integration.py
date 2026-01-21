import json
import os
from pathlib import Path
import pytest
from pulumi_autodoc.utils import engineer_prompt, get_gemini_summary


@pytest.fixture
def api_key():
    return os.environ.get("GEMINI_API_KEY")


@pytest.fixture
def endpoint():
    return os.environ.get("GEMINI_API_ENDPOINT")


@pytest.fixture
def test_data_path():
    return Path("tests/data")


def test_get_gemini_summary_integration_success(api_key, endpoint):
    if not api_key or not endpoint:
        pytest.skip(
            "GEMINI_API_KEY and GEMINI_API_ENDPOINT must be set in environment variables"
        )
    prompt = "Briefly explain why the sky is blue."
    summary = get_gemini_summary(prompt, api_key, endpoint)
    print(summary)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "sky" in summary.lower()


def test_get_gemini_summary_integration_success2(api_key, endpoint):
    if not api_key or not endpoint:
        pytest.skip(
            "GEMINI_API_KEY and GEMINI_API_ENDPOINT must be set in environment variables"
        )
    prompt = "Briefly explain why the sky is blue."
    summary = get_gemini_summary(prompt, api_key, endpoint)
    print(summary)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "sky" in summary.lower()


def test_get_gemini_summary_integration_fail(api_key, endpoint):
    if not api_key or not endpoint:
        pytest.skip(
            "GEMINI_API_KEY and GEMINI_API_ENDPOINT must be set in environment variables"
        )
    prompt = "Briefly explain why the sky is blue."
    summary = get_gemini_summary(prompt, api_key, endpoint)
    print(summary)
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "blahblahblah" not in summary.lower()


@pytest.fixture
def test_stack_json(test_data_path):
    return test_data_path / "inputs/dev.json"


@pytest.fixture
def test_stack_code(test_data_path):
    return test_data_path / "inputs" / "api_deployment.py"


@pytest.fixture
def code_snippet():
    return """
        listener = aws.lb.Listener(
            RESOURCE_NAME,
            load_balancer_arn=load_balancer.arn,
            port=443,
            protocol="HTTPS",
            ssl_policy="ELBSecurityPolicy-2016-08",
            certificate_arn=certificate.arn,
            default_actions=[
                {
                    "type": "forward",
                    "target_group_arn": target_group.arn,
                }
            ],
        )
        """


def test_gemini_summary_from_json_to_markdown(
    test_data_path, api_key, endpoint, test_stack_json
):
    if not api_key or not endpoint:
        pytest.skip(
            "GEMINI_API_KEY and GEMINI_API_ENDPOINT must be set in environment variables"
        )

    # Read JSON and engineer prompt
    with open(test_stack_json) as f:
        stack_json = f.read()

    prompt = engineer_prompt(stack_json)
    print(prompt)
    summary = get_gemini_summary(prompt, api_key, endpoint)

    # Write markdown result
    md_path = test_data_path / "outputs" / "dev-summary.md"
    with open(md_path, "w") as f:
        f.write(f"# Pulumi Stack Summary\n\n{summary}\n")

    # Check markdown file was written and contains summary
    with open(md_path) as f:
        content = f.read()
    assert summary in content
    assert content.startswith("# Pulumi Stack Summary")
