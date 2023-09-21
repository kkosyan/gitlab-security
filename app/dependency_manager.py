import dynaconf

from domain.file_writer import ExcelWriter
from domain.members_extractor import MembersExtractor
from usecase.extract_project_members import ExtractProjectsMembers


class DependencyManager:
    extract_project_members: ExtractProjectsMembers


class LocalDependencyManager(DependencyManager):
    def __init__(self, settings: dynaconf.Dynaconf):
        members_extractor = MembersExtractor(
            url=settings.gitlab_url,
            token=settings.gitlab_token,
        )
        file_writer = ExcelWriter(
            file_dir=settings.report_dir,
        )

        self.data_emulator_for_single_table = ExtractProjectsMembers(
            members_extractor=members_extractor,
            file_writer=file_writer,
        )
