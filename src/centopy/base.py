"""
    Package "centopy"

    This module provides package's base logic, factories and abstractions
"""
import logging
from pathlib import Path

logger = logging.getLogger('standard')


class BaseFilesManager:
    """
    A base class for managing files in a specified directory.

    Parameters
    ----------
    folder_path : str
        The path of the directory where the files will be stored.

    Attributes
    ----------
    folder_path : Path object
        The absolute path to the directory where the files are stored.
    file_state : dict
        A dictionary that keeps track of the state of each file.

    Methods
    -------
    file_path(file_name: str) -> Path object:
        Returns the absolute path to the specified file.
    get_file_state(file_name: str) -> str:
        Returns the state of the specified file.
    list_files() -> List[str]:
        Returns a list of the names of all files in the directory.
    delete_file(file_name: str) -> None:
        Deletes the specified file from the directory.
    """
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.file_state = {}
        try:
            self.folder_path.mkdir(parents=True, exist_ok=True)
        except OSError as err:
            raise ValueError(f"Invalid folder path: {folder_path}") from err

    def file_path(self, file_name):
        """
        Returns the absolute path to the specified file.

        Parameters
        ----------
        file_name : str
            The name of the file.

        Returns
        -------
        Path
            The absolute path to the specified file.
        """
        return self.folder_path / file_name

    def get_file_state(self, file_name):
        """
        Returns the state of the specified file.

        Parameters
        ----------
        file_name : str
            The name of the file.

        Returns
        -------
        str
            The state of the specified file. If the file has not been accessed, the state is "unknown".
        """
        return self.file_state.get(file_name, ["unknown"])[-1]

    def list_files(self):
        """
        Returns a list of the names of all files in the directory.

        Returns
        -------
        List[str]
            A list of the names of all files in the directory.
        """
        return [f.name for f in self.folder_path.glob("*") if f.is_file()]

    def delete_file(self, file_name):
        """
        Deletes the specified file from the directory.

        Parameters
        ----------
        file_name : str
            The name of the file.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        """
        file_path = self.file_path(file_name)
        if file_path.exists():
            file_path.unlink()
            self.file_state.setdefault(file_name, []).append("deleted")
        else:
            logger.warning("File not found: %s. Nothing to delete", file_name)

    def __str__(self):
        files = self.list_files()
        file_info = []
        for file in files:
            file_state = self.get_file_state(file)
            file_info.append(f"{file}: {file_state}")
        text = f"Working dir: {self.folder_path.absolute()}\n"
        text+= "\n".join(file_info)
        return text


class BaseHandleData:
    def __init__(self,):
        pass
