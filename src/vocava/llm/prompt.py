import json
import pathlib
import string

PROMPTS_PATH = pathlib.Path(__file__).parent / "prompts"


def load_prompt(name: str, **kwargs):
    with open(PROMPTS_PATH / f"{name}.md", "r") as file:
        prompt_template = string.Template(file.read())
    return prompt_template.substitute(**kwargs)


def extract_json(content):
    content = content.replace("```json", "").replace("```", "")
    start = content.find("{")
    payload = content[start:]
    try:
        return json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        raise ValueError("Invalid JSON returned by model") from e
