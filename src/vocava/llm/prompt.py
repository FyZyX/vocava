import pathlib
import string

PROMPTS_PATH = pathlib.Path(__file__).parent / "prompts"


def load_prompt(name: str, **kwargs):
    with open(PROMPTS_PATH / f"{name}.md", "r") as file:
        prompt_template = string.Template(file.read())
    return prompt_template.substitute(**kwargs)
