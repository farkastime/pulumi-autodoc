import logging
import requests

logger = logging.getLogger(__name__)


def get_gemini_summary(prompt, api_key, endpoint):
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    logger.debug(f"Sending request to Gemini API at {endpoint}")
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    summary = result["candidates"][0]["content"]["parts"][0]["text"]
    return summary


def engineer_prompt(stack_json) -> str:
    preamble = """
        Provide a structured summary of the following Pulumi stack JSON in Markdown format.
        Do not include any preamble or explanation, just provide the summary of all the resources.
    """
    return f"{preamble}:\n\n{stack_json}\n\n"
