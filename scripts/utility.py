from pathlib import Path
import shutil
import sys
from jinja2 import Environment
import logger

log = logger.get_logger()

def render_pages(env: Environment, pages_dir: Path, output_dir: Path):
    for html_file in pages_dir.rglob("*.html"):
        relative_path = html_file.relative_to(pages_dir)
        output_file = output_dir / relative_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        template = env.get_template(str(relative_path).replace("\\", "/"))
        render = template.render()

        output_file.write_text(render, encoding="utf-8")
        log.info(f"Rendering {relative_path.name}")

def copy_assets(base_dir: Path, output_dir: Path, folders: list[str]):
    missing_folders = []

    for folder in folders:
        source = base_dir / folder
        destination = output_dir / folder

        if not source.exists():
            missing_folders.append(folder)
            continue

        if destination.exists():
            shutil.rmtree(destination)

        shutil.copytree(source, destination)
        log.info(f"Copied {folder} folder to output folder")

    if missing_folders:
        for folder in missing_folders:
            log.error(f"{folder} folder does not exist")
        sys.exit(1)