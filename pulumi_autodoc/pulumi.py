import os
from pathlib import Path


def get_pulumi_stack_jsons(stack_dir: Path) -> list[Path]:
    stack_dir = Path(stack_dir).resolve()
    json_files = []
    for dirpath, dirnames, filenames in os.walk(stack_dir):
        for filename in filenames:
            if filename.endswith("json"):
                abs_path = Path(dirpath) / filename
                rel_path = abs_path.relative_to(stack_dir)
                json_files.append(rel_path)
    return json_files
