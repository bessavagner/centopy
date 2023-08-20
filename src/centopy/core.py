"""
    Package "centopy"

    This module provides package's api
"""

import logging
from .base import BaseFilesManager

logger = logging.getLogger('standard')

class FilesManager(BaseFilesManager):
    """
    A class for managing files in a specified folder.

    Parameters
    ----------
    folder_path : str
        The path to the folder to manage.

    Attributes
    ----------
    file_state : dict
        A dictionary containing the state of each file that has been saved or
        loaded.

    """
    def __init__(self, folder_path: str, *args, **kwargs):
        super().__init__(folder_path, *args, **kwargs)

    def write(
            self,
            file_name,
            file_contents,
            encoding="utf-8",
            **kwargs
    ):
        """
        Save the contents to a file.

        Parameters
        ----------
        file_name : str
            The name of the file to save.
        file_contents : str
            The contents to save to the file.
        encoding : str, optional
            The encoding of the file, by default "utf-8".
        **kwargs
            Additional keyword arguments to pass to the open() function.

        """
        with open(
            self.file_path(file_name), 'w', encoding=encoding, **kwargs
        ) as file_:
            file_.write(file_contents)
        state = self.file_state.setdefault(file_name, [])
        state.append("saved")
        self.file_state[file_name] = state

    def read(self, file_name, mode='r', encoding="utf-8", **kwargs):
        """
        Load the contents of a file.

        Parameters
        ----------
        file_name : str
            The name of the file to load.
        encoding : str, optional
            The encoding of the file, by default "utf-8".
        **kwargs
            Additional keyword arguments to pass to the open() function.

        Returns
        -------
        str or None
            The contents of the file, or None if the file was not found.

        """
        file_contents = None
        state = self.file_state.setdefault(file_name, [])
        try:
            with open(
                self.file_path(file_name), mode, encoding=encoding, **kwargs
            ) as file_:
                file_contents = file_.read()
            state.append("loaded")
        except FileNotFoundError:
            state.append("failed")
            logger.error("File not found: %s. Returning None", file_name)
        self.file_state[file_name] = state
        return file_contents
