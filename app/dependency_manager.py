import pathlib

import dynaconf

from domain.file_writer import ExcelWriter
from domain.members_comparison import MembersComparison
from domain.members_extractor import MembersExtractor
from usecase.extract_project_members import ExtractProjectsMembers
from usecase.project_members_comparison import ProjectsMembersComparison


class DependencyManager:
    extract_project_members: ExtractProjectsMembers
    project_members_comparison: ProjectsMembersComparison


class LocalDependencyManager(DependencyManager):
    def __init__(self, settings: dynaconf.Dynaconf):
        members_extractor = MembersExtractor(
            url=settings.gitlab_url,
            token=settings.gitlab_token,
        )
        file_writer = ExcelWriter(
            file_dir=pathlib.Path(settings.report_dir),
        )
        members_comparison = MembersComparison()

        self.extract_project_members = ExtractProjectsMembers(
            members_extractor=members_extractor,
            file_writer=file_writer,
        )
        self.project_members_comparison = ProjectsMembersComparison(
            file_writer=file_writer,
            members_extractor=members_extractor,
            members_comparison=members_comparison,
        )
