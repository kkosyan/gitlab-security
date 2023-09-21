import abc
import pathlib
from datetime import date

import pandas as pd


class FileWriter:
    @abc.abstractmethod
    def save(self, data: pd.DataFrame):
        ...


class ExcelWriter(FileWriter):
    def __init__(self, file_dir: pathlib.Path):
        self._file_dir = file_dir

    def _setup(self):
        self._file_dir.parent.mkdir(parents=True, exist_ok=True)

    def save(self, data: pd.DataFrame):
        if not self._file_dir.exists():
            self._setup()

        file_path = self._file_dir / f'projects_members_on_{date.today()}.xlsx'
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        data.to_excel(writer)
