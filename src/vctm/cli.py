import getpass
import os

import click

from vctm.business.database import DatabaseCreateExecutor

from vctm.business.organisation import OrganisationAddExecutor
from vctm.business.organisation import OrganisationDeleteExecutor
from vctm.business.organisation import OrganisationListExecutor

from vctm.business.project import ProjectAddExecutor
from vctm.business.project import ProjectDeleteExecutor
from vctm.business.project import ProjectListExecutor
from vctm.business.project import ProjectListByOrganisationExecutor

from vctm.business.directory import DirectoryAddExecutor
from vctm.business.directory import DirectoryDeleteExecutor
from vctm.business.directory import DirectoryInfoExecutor
from vctm.business.directory import DirectoryListExecutor

from vctm.business.entry import EntryAddExecutor
from vctm.business.entry import EntryListExecutor


def create_context() -> hash:
    context = {}
    context["interface"] = "cli"
    context["username"] = getpass.getuser()

    return context


@click.group()
def cli() -> None:
    pass


@cli.group()
def database() -> None:
    """Database commands"""
    pass


@database.command("create")
def database_create() -> None:
    """Create a new database."""
    context = create_context()
    executor = DatabaseCreateExecutor()
    executor.execute(context)


@cli.group()
def organisation() -> None:
    """Organisation commands"""
    pass


@organisation.command("add")
@click.argument("name")
def organisation_add(name: str) -> None:
    """Add a new organisation."""
    context = create_context()
    context["organisation_name"] = name
    executor = OrganisationAddExecutor()
    executor.execute(context)


@organisation.command("delete")
@click.argument("name")
def organisation_delete(name: str) -> None:
    """Delete a organisation."""
    context = create_context()
    context["organisation_name"] = name
    executor = OrganisationDeleteExecutor()
    executor.execute(context)


@organisation.command("list")
def project_list() -> None:
    """List all organisation."""
    context = create_context()
    executor = OrganisationListExecutor()
    executor.execute(context)
    organisations = context["organisations"]

    print("| " + "id".rjust(3) + " | " + "organisation".rjust(12) + " |")
    print("| " + "-" * 3 + " | " + "-" * 12 + " |")
    for organisation in organisations:
        print(
            f"| {organisation.organisation_id:3d} | {organisation.organisation_name: >12} |"
        )


@cli.group()
def project() -> None:
    """Project commands"""
    pass


@project.command("add")
@click.argument("organisation")
@click.argument("name")
def project_add(organisation: str, name: str) -> None:
    """Add a new project."""
    context = create_context()
    context["organisation_name"] = organisation
    context["project_name"] = name
    executor = ProjectAddExecutor()
    executor.execute(context)


@project.command("delete")
@click.argument("organisation")
@click.argument("name")
def project_delete(organisation: str, name: str) -> None:
    """Delete a project."""
    context = create_context()
    context["organisation_name"] = organisation
    context["project_name"] = name
    executor = ProjectDeleteExecutor()
    executor.execute(context)


@project.command("list")
@click.option("-o", "--organisation", help="name of the organisation")
def project_list(organisation: str) -> None:
    """List all projects."""
    context = create_context()

    if organisation:
        context["organisation_name"] = organisation
        executor = ProjectListByOrganisationExecutor()
    else:
        executor = ProjectListExecutor()

    executor.execute(context)

    projects = context["projects"]

    print(
        "| "
        + "id".rjust(3)
        + " | "
        + "organisation".rjust(12)
        + " | "
        + "project".ljust(12)
        + " |"
    )
    print("| " + "-" * 3 + " | " + "-" * 12 + " | " + "-" * 12 + " |")
    for project in projects:
        organisation = project.organisation
        print(
            f"| {project.project_id:3d} | {organisation.organisation_name: >12} | {project.project_name: <12} |"
        )


@cli.group()
def directory() -> None:
    """Directory commands"""
    pass


@directory.command("add")
@click.argument("organisation")
@click.argument("project")
@click.argument("name", default=os.getcwd())
def directory_add(organisation: str, project: str, name: str) -> None:
    """Add a dirctory to an organisation and project"""
    context = create_context()
    context["organisation_name"] = organisation
    context["project_name"] = project
    context["directory_name"] = os.path.abspath(name)
    executor = DirectoryAddExecutor()
    executor.execute(context)


@directory.command("delete")
@click.argument("name", default=os.getcwd())
def directory_delete(name: str) -> None:
    """Delete a dirctory"""
    context = create_context()
    context["directory_name"] = os.path.abspath(name)
    executor = DirectoryDeleteExecutor()
    executor.execute(context)


@directory.command("info")
@click.argument("name", default=os.getcwd())
def directory_info(name: str) -> None:
    """Show information for the directory"""
    context = create_context()
    context["directory_name"] = os.path.abspath(name)
    executor = DirectoryInfoExecutor()
    executor.execute(context)

    directory = context["directory"]
    project_name = context["project_name"]
    organisation_name = context["organisation_name"]

    print(f"organisation: {organisation_name}")
    print(f"     project: {project_name}")
    print(f"   directory: {directory.directory_name}")


@directory.command("list")
def directory_list() -> None:
    """List all dirctories"""
    context = create_context()
    executor = DirectoryListExecutor()
    executor.execute(context)

    directories = context["directories"]

    print(
        "| "
        + "id".rjust(3)
        + " | "
        + "organisation".rjust(12)
        + " | "
        + "project".ljust(12)
        + " | "
        + " directory"
    )
    print("| " + "-" * 3 + " | " + "-" * 12 + " | " + "-" * 12 + " | " + "-" * 12)

    for directory in directories:
        project = directory.project
        organisation = project.organisation

        print(
            f"| {directory.directory_id:3d} | {organisation.organisation_name: >12} | {project.project_name: <12} | {directory.directory_name}"
        )


@cli.group()
def entry() -> None:
    """Entry commands"""
    pass


@entry.command("add")
@click.argument("name", default=os.getcwd())
def entry_add(name: str) -> None:
    """Add a entry to an organisation and project"""
    context = create_context()
    context["directory_name"] = os.path.abspath(name)
    executor = EntryAddExecutor()
    executor.execute(context)


@entry.command("list")
def entry_list() -> None:
    """List all entries"""
    context = create_context()
    executor = EntryListExecutor()
    executor.execute(context)

    entries = context["entries"]

    print(
        "| "
        + "id".rjust(3)
        + " | "
        + "organisation".rjust(12)
        + " | "
        + "project".ljust(12)
        + " | "
        + " directory"
    )
    print("| " + "-" * 3 + " | " + "-" * 12 + " | " + "-" * 12 + " | " + "-" * 12)

    for entry in entries:
        project = entry.project
        organisation = project.organisation

        print(
            f"| {entry.entry_id:3d} | {organisation.organisation_name: >12} | {project.project_name: <12} | {entry.entry_name}"
        )


if __name__ == "__main__":
    cli()
