import pathlib
import time
from datetime import date

import gitlab
import pandas as pd
import pytest

from app.config import get_settings
from domain.file_writer import ExcelWriter
from domain.members_extractor import MembersExtractor
from usecase.extract_project_members import ExtractProjectsMembers

settings = get_settings(env_for_dynaconf='testing')

excel_writer = ExcelWriter(
    file_dir=pathlib.Path(settings.report_dir),
)
members_extractor = MembersExtractor(
    token=settings.gitlab_token,
    url=settings.gitlab_url,
)
extract_projects_members = ExtractProjectsMembers(
    file_writer=excel_writer,
    members_extractor=members_extractor,
)


@pytest.mark.e2e
class TestExtractProjectMembers:
    expected_result = pd.DataFrame({})

    @staticmethod
    def prepare_environment():
        gl = gitlab.Gitlab(url=settings.gitlab_url, private_token=settings.gitlab_token)
        project1 = gl.projects.create({'name': 'project1', 'id': 1})
        project2 = gl.projects.create({'name': 'project2', 'id': 2})
        project3 = gl.projects.create({'name': 'project3', 'id': 3})
        user1 = gl.users.create({'email': 'user1@gl.com',
                                 'password': 'DplFngsbAX',
                                 'username': 'user1',
                                 'name': 'user1'})
        user2 = gl.users.create({'email': 'user2@gl.com',
                                 'password': 'MBawoMdLnz',
                                 'username': 'user2',
                                 'name': 'user2'})
        user3 = gl.users.create({'email': 'user3@gl.com',
                                 'password': '4YsOh4deKe',
                                 'username': 'user3',
                                 'name': 'user3'})

        project1.members.create({'user_id': user1.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})
        project1.members.create({'user_id': user2.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})
        project1.members.create({'user_id': user3.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})

        project2.members.create({'user_id': user1.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})
        project2.members.create({'user_id': user2.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})

        project3.members.create({'user_id': user1.id, 'access_level': gitlab.const.AccessLevel.DEVELOPER})

    @staticmethod
    def clear_environment():
        gl = gitlab.Gitlab(url=settings.gitlab_url, private_token=settings.gitlab_token)
        projects = gl.projects.list(get_all=True)
        for project in projects:
            project.delete()

        users = gl.users.list()
        for user in users:
            user.delete()

    def test_extract_members(self):
        self.clear_environment()
        time.sleep(10)
        self.prepare_environment()
        extract_projects_members.execute()

        result = pd.read_excel(settings.report_dir / f'projects_members_on_{date.today()}.xlsx')

        assert result == self.expected_result
