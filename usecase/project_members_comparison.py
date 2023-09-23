from domain.file_writer import FileWriter
from domain.members_comparison import MembersComparison
from domain.members_extractor import MembersExtractor


class ProjectsMembersComparison:
    def __init__(self, file_writer: FileWriter, members_extractor: MembersExtractor,
                 members_comparison: MembersComparison):
        self._file_writer = file_writer
        self._members_extractor = members_extractor
        self._members_comparison = members_comparison

    def execute(self, file_name: str):
        fact_data = self._members_extractor.get_members()
        comparison_result = self._members_comparison.execute_comparison(fact_members=fact_data, file_name=file_name)
        self._file_writer.save_multiple_sheets(tables=comparison_result)
