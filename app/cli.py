import click

from app.config import get_settings
from app.dependency_manager import LocalDependencyManager, DependencyManager


def build_cli() -> click.Command:
    pass_context = click.make_pass_decorator(LocalDependencyManager)

    @click.group()
    @click.pass_context
    @click.option('--env', '-e', 'env_for_dynaconf', default='testing', help='Set environment for Dynaconf')
    def cli(ctx: click.Context, env_for_dynaconf: str):
        settings = get_settings(env_for_dynaconf=env_for_dynaconf)
        ctx.obj = LocalDependencyManager(settings=settings)

    @cli.command('extract-projects-members')
    @pass_context
    def emulate_single_table(context: DependencyManager):
        return context.extract_project_members.execute()

    return cli
