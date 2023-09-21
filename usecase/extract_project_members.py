from domain.file_writer import FileWriter
from domain.members_extractor import MembersExtractor


class ExtractProjectsMembers:
    def __init__(self, file_writer: FileWriter, members_extractor: MembersExtractor):
        self._file_writer = file_writer
        self._members_extractor = members_extractor

    def execute(self):
        data = self._members_extractor.get_members()
        self._file_writer.save(data=data)
