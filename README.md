# centopy

API for managing files in a specified folder.

## Installation

```bash
$ pip install centopy
```

## Usage

### FilesManager

To use the FilesManager class in your Python script or project, import it as follows:

```python
from centopy import FilesManager
```
#### Creating a FilesManager Instance

To create an instance of the FilesManager class, provide the folder path where you want to manage the files:

```python
folder_path = "/path/to/folder"
file_manager = FilesManager(folder_path)
```

#### Saving and Loading Files

You can save and load file contents using the save_file and load_file methods, respectively:

```python
file_name = "example.txt"
file_contents = "Hello, world!"

# Save file contents to the specified file
file_manager.save_file(file_name, file_contents)

# Load file contents from the specified file
loaded_contents = file_manager.load_file(file_name)
```

#### Reading and Writing Files

You can also directly read from and write content to files using the read_file and write_file methods:

```python
file_name = "example.txt"
file_contents = "Hello, world!"

# Write contents to the specified file
file_manager.write_file(file_name, file_contents)

# Read contents from the specified file
read_contents = file_manager.read_file(file_name)
```

#### Handling File States

The FilesManager class keeps track of the state of each file that has been saved or loaded. You can check the state of a file using the get_file_state method:

```python
file_name = "example.txt"
state = file_manager.get_file_state(file_name)
print(f"File state for '{file_name}': {state}")
```

**Note:** The state is represented as a list of events. For example, if a file is saved and loaded, the state attribute (`file_manager.file_state[file_name]`) will be `["saved", "loaded"]`.

#### Handling Exceptions

When loading a file, if the specified file is not found, the load_file method returns None and logs an error message using the logging module. To handle such cases, you can check if the loaded contents are None:

```python
file_name = "nonexistent_file.txt"
loaded_contents = file_manager.load_file(file_name)

if loaded_contents is None:
    print(f"The file '{file_name}' was not found.")
```

### Compressor:

The class `centopy.Compressor` is an api to the `zipfile.ZipFile` context manager. You can use a custom extension when instantiating.

#### Writing and appending files

```python
archive = centopy.Compressor('file', extension='customzip', wdir='data')
```

An object `centopy.Compressor` has a attribute as an instance of `centopy.FilesManager`.

```python
print(archive.manager.list_files())
```
```bash
['file.customzip', 'data.bin', 'hello.txt']
```

```Python
content = 'Hello, centopy!'
archive.write('hello.txt', content=content)

# list files inside archive
print(archive.namelist())
```

```bash
['hello.txt']
```

#### Binary Data Compression

```python
# Create a Compressor object
compressor = Compressor("bin_archive")

# Write binary content to a new file and add it to the archive
binary_data = b'\x00\x01\x02\x03\x04'
compressor.writeb("binary_data.bin", binary_data)

# Append binary content to an existing file in the archive
new_binary_data = b'\x05\x06\x07'
compressor.appendb("binary_data.bin", new_binary_data)

# Read the binary content of a file from the archive
binary_content = compressor.read("binary_data.bin", as_text=False)

print("Binary content:", binary_content)

```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`centopy` was created by Vagner Bessa. Vagner Bessa retains all rights to the source and it may not be reproduced, distributed, or used to create derivative works.

## Credits

`centopy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
