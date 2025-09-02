
import typer
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

app = typer.Typer()

TEMPLATE_DIR = Path(__file__).parent / "template"

@app.callback(invoke_without_command=True)
def main(name: str = typer.Argument(..., help="The name of the project to create.")):
    """Creates a new FastAPI project with a layered architecture."""
    project_dir = Path(os.getcwd()) / name
    template_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

    print(f"Creating project directory: {project_dir}")
    os.makedirs(project_dir, exist_ok=True)

    # Walk through the template directory
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        rel_root = Path(root).relative_to(TEMPLATE_DIR)
        dest_root = project_dir / rel_root

        # Create directories
        for d in dirs:
            # Skip __pycache__ directories
            if d == "__pycache__":
                continue
            os.makedirs(project_dir / rel_root / d, exist_ok=True)

        # Process files
        for f in files:
            src_path = Path(root) / f
            dest_path = project_dir / rel_root / f.replace(".jinja", "")

            if f.endswith(".jinja"):
                template = template_env.get_template(str(src_path.relative_to(TEMPLATE_DIR)))
                rendered_content = template.render(project_name=name)
                with open(dest_path, "w") as out_file:
                    out_file.write(rendered_content)
            else:
                shutil.copy(src_path, dest_path)

    print(f"Project {name} created successfully!")
    print(f"To get started:")
    print(f"  cd {name}")
    print(f"  # Install dependencies using your package manager (e.g., pip, poetry, hatch)")
    print(f"  # Run migrations with 'aerich init-db' and 'aerich migrate'")
    print(f"  # Start the server with 'uvicorn app.main:app --reload'")

if __name__ == "__main__":
    app()
