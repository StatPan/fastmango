import typer
import pathlib
import jinja2
import os

TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "template" / "basic"

def new(
    name: str = typer.Argument(..., help="The name of the project to create."),
    template: str = typer.Option("basic", "--template", "-t", help="The template to use for the project."),
):
    """
    Creates a new FastMango project directory structure from a template.
    """
    typer.echo(f"🚀 Creating new FastMango project: {name}")

    project_dir = pathlib.Path.cwd() / name
    if project_dir.exists():
        typer.secho(f"Error: Directory '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(1)

    project_dir.mkdir()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)))

    context = {"project_name": name}

    for template_file in TEMPLATE_DIR.glob("*.jinja"):
        template = env.get_template(template_file.name)
        rendered_content = template.render(context)

        # Remove .jinja extension for the output file
        output_filename = template_file.stem
        output_path = project_dir / output_filename

        output_path.write_text(rendered_content)
        typer.echo(f"  ✅ Created {output_path}")

    typer.secho(f"\n🎉 Project '{name}' created successfully!", fg=typer.colors.GREEN)
    typer.echo("\nNext steps:")
    typer.echo(f"  1. cd {name}")
    typer.echo(f"  2. (Optional) Create a virtual environment and install dependencies.")
    typer.echo(f"  3. Run `fastmango run` to start the development server.")


def create_new_project(name: str, template: str = "basic") -> None:
    """
    Create a new FastMango project.
    
    Args:
        name: The name of the project to create
        template: The template to use (default: "basic")
    """
    # Call the typer app programmatically
    typer.echo(f"🚀 Creating new FastMango project: {name}")
    
    project_dir = pathlib.Path.cwd() / name
    if project_dir.exists():
        typer.secho(f"Error: Directory '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    project_dir.mkdir()
    
    # For now, just create a basic structure
    # In the future, this would use templates
    (project_dir / "main.py").write_text("""from fastmango import MangoApp

app = MangoApp()

@app.get("/")
async def root():
    return {"message": "Hello, FastMango!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
""")
    
    typer.secho(f"\n🎉 Project '{name}' created successfully!", fg=typer.colors.GREEN)
