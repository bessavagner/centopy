"""
    Package "centopy"

    This module provides package's api
"""
import os
import logging
import zipfile
import tempfile
import shutil

from pathlib import Path

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
        A `loaded' state simply means that the contents of the file were saved
        in a variable

    """
    def __init__(self, folder_path: str, *args, **kwargs):
        super().__init__(folder_path, *args, **kwargs)

    def _open_write(
            self,
            file_name: str,
            file_contents: bytes,
            mode='w',
            encoding="utf-8",
            **kwargs):
        """
        Save the contents to a file.

        Parameters
        ----------
        file_name : str
            The name of the file to save.
        file_contents : str
            The contents to save to the file.
        mode: str, optional
            Specifies the mode in which the file is opened, by default 'w'.
        encoding : str, optional
            The encoding of the file, by default "utf-8".
        **kwargs
            Additional keyword arguments to pass to the open() function.

        """
        with open(
            self.file_path(file_name), mode, encoding=encoding, **kwargs
        ) as file_:
            file_.write(file_contents)
        state = self.file_state.setdefault(file_name, [])
        state.append("saved")
        self.file_state[file_name] = state

    def _open_read(self, file_name, mode='r', encoding="utf-8", **kwargs):
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
        

    def write(
            self,
            file_name: str,
            file_contents: bytes,
            encoding="utf-8",
            **kwargs):
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
        self._open_write(file_name, file_contents, 'w', encoding, **kwargs)

    def writeb(
            self,
            file_name: str,
            file_contents: bytes,
            **kwargs
    ):
        """
        Save the binary contents to a file.

        Parameters
        ----------
        file_name : str
            The name of the file to save.
        file_contents : bytes
            The contents to save to the file.
        encoding : str, optional
            The encoding of the file, by default "utf-8".
        **kwargs
            Additional keyword arguments to pass to the open() function.

        """
        self._open_write(
            file_name, file_contents, 'wb', encoding=None, **kwargs
        )

    def append(
            self,
            file_name: str,
            file_contents: bytes,
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
        self._open_write(file_name, file_contents, 'a', encoding, **kwargs)

    def appendb(
            self,
            file_name: str,
            file_contents: bytes,
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
        self._open_write(file_name, file_contents, 'ab', encoding=None, **kwargs)

    def read(self, file_name, encoding="utf-8", **kwargs):
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
        return self._open_read(file_name, encoding=encoding, **kwargs)

    def readb(self, file_name: str, **kwargs):
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
        return self._open_read(file_name, mode='rb', encoding=None, **kwargs)


class Compressor:
    def __init__(self,
                 filename: str,
                 wdir: str = '',
                 extension: str = 'zip') -> None:
        """
        Initialize the Compressor object.

        Parameters
        ----------
        filename : str
            The base filename for the compressed archive.
        wdir : str, optional
            The working directory path where the archive will be managed, by default ''.
        extension : str, optional
            The extension for the compressed archive, by default 'zip'.
        """
        self.extension = extension
        self.filename = f"{filename}.{self.extension}"
        self.manager = FilesManager(wdir)
        self.file_path = self.manager.folder_path / self.filename
        self.members = {}
        if self.file_path.name not in self.manager.list_files():
            self.clean()
        else:
            with zipfile.ZipFile(self.file_path, mode='r') as archive:
                for name in archive.namelist():
                    self.members[Path(name).name] = name

    def clean(self,):
        with zipfile.ZipFile(self.file_path, mode="w") as _:
            pass

    def path(self,):
        """
        Get the full path to the compressed archive file.

        Returns
        -------
        Path
            The full path to the compressed archive file.
        """
        return self.manager.folder_path / self.file_path

    def namelist(self,):
        """
        Get a list of filenames present in the compressed archive.

        Returns
        -------
        List[str]
            A list of filenames present in the compressed archive.
        """
        if self.file_path.name in self.manager.list_files():
            with zipfile.ZipFile(self.file_path, mode="r") as archive:
                return [Path(name).name for name in archive.namelist()]
        return []

    def add(self, filename: str, delete_source=False, mode='a') -> None:
        """
        Add a file to the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to be added.
        delete_source : bool, optional
            If True, delete the source file after adding, by default True.
        mode : str, optional
            The mode to open the compressed archive, by default 'a'.
        """
        if filename in self.manager.list_files():
            with zipfile.ZipFile(self.file_path, mode=mode) as archive:
                archive.write(self.manager.file_path(filename), filename)
                if delete_source:
                    self.manager.delete_file(filename)
                self.members[filename] = archive.namelist()[-1]
        else:
            logger.warning(
                'File %s not found in working directory %s',
                filename,
                self.manager.folder_path
            )

    def add_from(self, filename: str, delete_source=False, mode='a') -> None:
        """
        Add a file to the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to be added.
        delete_source : bool, optional
            If True, delete the source file after adding, by default True.
        mode : str, optional
            The mode to open the compressed archive, by default 'a'.
        """
        file_path = Path(filename)
        if file_path.exists():
            with zipfile.ZipFile(self.file_path, mode=mode) as archive:
                archive.write(file_path, file_path.name)
                if delete_source:
                    if file_path.exists():
                        os.remove(file_path)
                self.members[file_path.name] = archive.namelist()[-1]
        else:
            logger.warning(
                'File %s not found.',
                file_path
            )

    def write(self,
              filename: str,
              content: str,
              delete_source=False,
              mode='a') -> None:
        """
        Write content to a new file and add it to the compressed archive,
        or overwrite if it's already a member of archive.

        Parameters
        ----------
        filename : str
            The name of the file to be written and added.
        content : str
            The content to be written to the new file.
        delete_source : bool, optional
            If True, delete the source file after adding, by default True.
        mode : str, optional
            The mode to open the compressed archive, by default 'a'.
        """
        self.manager.write(filename, content)
        if filename in self.namelist():
            self.append(filename, content='')
            return
        self.add(filename, delete_source=delete_source, mode=mode)

    def writeb(self,
               filename: str,
               content: bytes,
               delete_source=False,
               mode='a') -> None:
        """
        Write bytes content to a new file and add it to the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to be written and added.
        content : bytes
            The bytes content to be written to the new file.
        delete_source : bool, optional
            If True, delete the source file after adding, by default True.
        mode : str, optional
            The mode to open the compressed archive, by default 'a'.
        """
        self.manager.writeb(filename, content)
        if filename in self.namelist():
            self.appendb(filename, content=b'')
            return
        self.add(filename, delete_source=delete_source, mode=mode)

    def append(self, filename: str, content: str) -> None:
        """
        Append content to an existing text file within the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to which content will be appended.
        content : str
            The content to be appended to the existing text file.
        """
        temp_dir = Path(tempfile.mkdtemp())
        data = self.read(filename)
        for member in self.namelist():
            if member != filename:
                self.extract(member, path=temp_dir)
        if filename in self.namelist():
            with zipfile.ZipFile(self.file_path, mode="w") as archive:
                with archive.open(self.members[filename], mode='w') as member:
                    data += content
                    member.write(data.encode('utf-8'))
            for member in temp_dir.glob('**/*'):
                self.add_from(member, delete_source=True)
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        else:
            logger.warning(
                'File %s not found in working directory %s',
                filename,
                self.manager.folder_path
            )

    def appendb(self, filename: str, content: bytes) -> None:
        """
        Append content to an existing binary file within the compressed
        archive.

        Parameters
        ----------
        filename : str
            The name of the file to which content will be appended.
        content : bytes
            The bytes content to be appended to the existing binary file.
        """
        temp_dir = Path(tempfile.mkdtemp())
        data = self.read(filename, as_text=False)
        for member in self.namelist():
            if member != filename:
                self.extract(member, path=temp_dir)
        if filename in self.namelist():
            with zipfile.ZipFile(self.file_path, mode="w") as archive:
                with archive.open(self.members[filename], mode='w') as member:
                    data += content
                    member.write(data)
            for member in temp_dir.glob('**/*'):
                self.add_from(member, delete_source=True)
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        else:
            logger.warning(
                'File %s not found in working directory %s',
                filename,
                self.manager.folder_path
            )

    def read(self, filename: str, as_text=True) -> str | bytes:
        """
        Read the content of a file within the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to be read.
        as_text : bool, optional
            If True, return content as text, otherwise as bytes, by default True.

        Returns
        -------
        str or bytes
            The content of the specified file.
        """
        with zipfile.ZipFile(self.file_path, mode="r") as archive:
            with archive.open(self.members[filename], mode='r') as member:
                data = member.read()
                if as_text:
                    return data.decode('utf-8')
                return data

    def readb(self, filename: str) -> str | bytes:
        """
        Read the content of a file within the compressed archive.

        Parameters
        ----------
        filename : str
            The name of the file to be read.
        as_text : bool, optional
            If True, return content as text, otherwise as bytes, by default True.

        Returns
        -------
        str or bytes
            The content of the specified file.
        """
        with zipfile.ZipFile(self.file_path, mode="r") as archive:
            with archive.open(self.members[filename], mode='r') as member:
                data = member.read()
                return data

    def extract(self, filename: str, path: str = None) -> str:
        """
        Extract a file from the compressed archive to the working directory.

        Parameters
        ----------
        filename : str
            The name of the file to be extracted.
        path : str
            Path to extract 'filename' to, by default self.manager.folder_path
        Returns
        -------
        str
            The path to the extracted file in the working directory.
        """
        if path is None:
            path = self.manager.folder_path
        with zipfile.ZipFile(self.file_path, mode="r") as archive:
            return archive.extract(
                self.members[filename],
                path=path
            )

    def remove(self, filename: str):
        temp_dir = Path(tempfile.mkdtemp())
        for member in self.namelist():
            if member != filename:
                self.extract(member, path=temp_dir)
        self.clean()
        for member in temp_dir.glob('**/*'):
            self.add_from(member)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def update(self, filename: str, delete_source=False):
        temp_dir = Path(tempfile.mkdtemp())
        for member in self.namelist():
            if member != filename:
                self.extract(member, path=temp_dir)
        self.clean()
        self.add(filename, delete_source=delete_source, mode='w')
        for member in temp_dir.glob('**/*'):
            self.add_from(member)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def update_from(self, filename: str, delete_source=False):
        temp_dir = Path(tempfile.mkdtemp())
        for member in self.namelist():
            if member != filename:
                self.extract(member, path=temp_dir)
        self.clean()
        self.add_from(filename, delete_source=delete_source, mode='w')
        for member in temp_dir.glob('**/*'):
            self.add_from(member)
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
