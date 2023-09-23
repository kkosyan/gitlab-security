import pathlib

import pandas as pd


class MembersComparison:
    @staticmethod
    def _get_expected_members(file_name: str) -> pd.DataFrame:
        return pd.read_excel(
            pathlib.Path(file_name),
            engine='openpyxl',
        )

    def execute_comparison(self, fact_members: pd.DataFrame, file_name: str) -> dict[str: pd.DataFrame]:
        expected_members = self._get_expected_members(file_name=file_name)
        merged = pd.merge(
            fact_members,
            expected_members,
            on='project_id',
            how='outer',
            suffixes=('_fact', '_expected'),
            indicator=True,
        )
        fact_columns = ['project_name_fact', 'project_members_fact']
        expected_columns = ['project_name_expected', 'project_members_expected']
        fact_only = merged[merged['_merge'] == 'left_only'][fact_columns]
        expected_only = merged[merged['_merge'] == 'right_only'][expected_columns]
        members_diff = (
            merged
            .loc[lambda df: df['_merge'] == 'both']
            .loc[lambda df: df['project_members_fact'] != df['project_members_expected']]
        )
        return {
            'Fact only': fact_only,
            'Expected only': expected_only,
            'Difference': members_diff[fact_columns + expected_columns],
        }
