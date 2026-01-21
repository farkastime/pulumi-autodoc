from pulumi_autodoc.utils import engineer_prompt, get_gemini_summary


def test_engineer_prompt_single_string():
    stack_json = '{"resources": [{"name": "bucket"}]}'
    result = engineer_prompt(stack_json)
    assert isinstance(result, str)
    assert "Summarize the following Pulumi stack JSON in Markdown format" in result
    assert stack_json in result
