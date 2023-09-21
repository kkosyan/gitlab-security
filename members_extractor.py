import gitlab


class MembersExtractor:
    def __init__(self, url: str, token: str):
        self._url = url
        self._token = token

    def _auth(self):
        return gitlab.Gitlab(url=self._url, private_token=self._token)

    def get_members(self):
        gl = self._auth()
        project = gl.projects.list(get_all=True)
        return project.members_all.list(get_all=True)
