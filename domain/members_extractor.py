import gitlab
import pandas as pd
from gitlab.v4.objects.projects import Project


class MembersExtractor:
    columns = [
        'project_id',
        'project_name',
        'project_members',
    ]

    def __init__(self, url: str, token: str):
        self._url = url
        self._token = token

    def _auth(self):
        return gitlab.Gitlab(url=self._url, private_token=self._token)

    @staticmethod
    def _get_members_names(project: Project) -> str:
        members = project.members_all.list(get_all=True)
        return ', '.join(member.username for member in members)

    def get_members(self) -> pd.DataFrame:
        gl = self._auth()
        projects = gl.projects.list(get_all=True)
        data = [
            (project.id, project.path_with_namespace, self._get_members_names(project=project))
            for project in projects
        ]
        return pd.DataFrame.from_records(data, columns=self.columns).sort_values(by=['project_id'])
