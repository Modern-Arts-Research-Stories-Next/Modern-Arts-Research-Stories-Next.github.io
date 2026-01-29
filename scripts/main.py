from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import argparse
import utility

class TypedArgs(argparse.Namespace):
    deploy: bool

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true")
    args: TypedArgs = parser.parse_args()

    if args.deploy:
        base_url = "https://Modern-Arts-Research-Stories-Next.github.io"
    else:
        base_url = "http://localhost:3000"

    base_dir = Path(__file__).parent.parent
    pages_dir = base_dir / "pages"
    partials_dir = base_dir / "partials"
    output_dir = base_dir / "Site"
    
    output_dir.mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader([str(pages_dir), str(partials_dir)]), autoescape=True)

    env.globals["base_url"] = base_url

    utility.render_pages(env=env, pages_dir=pages_dir, output_dir=output_dir)

    asset_folders = ["css"]
    utility.copy_assets(base_dir=base_dir, output_dir=output_dir, folders=asset_folders)

if __name__ == "__main__":
    main()