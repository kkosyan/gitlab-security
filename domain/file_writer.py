import abc
import pathlib
from datetime import date

import pandas as pd


class FileWriter:
    @abc.abstractmethod
    def save(self, data: pd.DataFrame):
        ...

    @abc.abstractmethod
    def save_multiple_sheets(self, tables: dict[str, pd.DataFrame]):
        ...


class ExcelWriter(FileWriter):
    def __init__(self, file_dir: pathlib.Path):
        self._file_dir = file_dir

    def _setup(self):
        self._file_dir.mkdir(parents=True, exist_ok=True)

    def save(self, data: pd.DataFrame):
        if not self._file_dir.exists():
            self._setup()

        file_path = self._file_dir / f'projects_members_on_{date.today()}.xlsx'
        with pd.ExcelWriter(file_path) as writer:
            data.to_excel(writer, index=False)

    def save_multiple_sheets(self, tables: dict[str, pd.DataFrame]):
        file_path = self._file_dir / f'projects_members_comparison_on_{date.today()}.xlsx'
        with pd.ExcelWriter(file_path) as writer:
            for name, data in tables.items():
                if not data.empty:
                    data.to_excel(writer, sheet_name=name, index=False)
                    sheet = writer.sheets[name]
                    sheet.write_row(0, 0, data.columns)
                    sheet.freeze_panes(1, 0)
