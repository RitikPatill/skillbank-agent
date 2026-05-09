import click


@click.group()
@click.version_option(package_name="skillbank-agent")
def cli():
    """SkillBank Agent — accumulative LLM agent with a growing skill library."""


@cli.command()
@click.argument("task")
@click.option("--verbose", "-v", is_flag=True, help="Show retrieved skills and generated code.")
def run(task, verbose):
    """Run TASK using the skill bank, then extract new skills from the solution."""
    raise click.ClickException("Not implemented yet")


@cli.command(name="list")
def list_skills():
    """List all skills currently stored in the skill bank."""
    raise click.ClickException("Not implemented yet")


@cli.command()
def reset():
    """Clear all skills from the skill bank."""
    raise click.ClickException("Not implemented yet")


@cli.command()
def demo():
    """Run 5 canonical demo tasks and print skill-bank growth stats."""
    raise click.ClickException("Not implemented yet")
