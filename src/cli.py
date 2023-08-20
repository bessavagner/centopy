import click
from apps import Files

@click.group()
@click.argument("directory", required=True)
@click.pass_context
def cli(ctx, directory):
    ctx.obj = Files(directory)

@cli.command()
@click.pass_context
def list_files(ctx):
    files = ctx.obj.run("list_files")
    click.echo("\n".join(files))

@cli.command()
@click.pass_context
@click.argument("file_name")
@click.option("--encoding", default="utf-8")
def load(ctx, file_name, encoding):
    contents = ctx.obj.run("load_file", file_name, encoding=encoding)
    click.echo(contents)

@cli.command()
@click.argument("file_name")
@click.argument("file_contents")
@click.option("--encoding", default="utf-8")
@click.pass_context
def save(ctx, file_name, file_contents, encoding):
    ctx.obj.run("save_file", file_name, file_contents, encoding=encoding)
    click.echo(f"Saved {file_name}")

@cli.command()
@click.argument("file_name")
@click.pass_context
def delete(ctx, file_name):
    ctx.obj.run("delete_file", file_name)
    click.echo(f"Deleted {file_name}")

if __name__ == "__main__":
    cli()    
