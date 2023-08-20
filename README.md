# centopy

API for managing files in a specified folder.

## Installation

```bash
$ pip install centopy
```

## Usage

### Importing the FilesManager

To use the FilesManager class in your Python script or project, import it as follows:

```python
from centopy import FilesManager
```
### Creating a FilesManager Instance

To create an instance of the FilesManager class, provide the folder path where you want to manage the files:

```python
folder_path = "/path/to/folder"
file_manager = FilesManager(folder_path)
```

### Saving and Loading Files

You can save and load file contents using the save_file and load_file methods, respectively:

```python
file_name = "example.txt"
file_contents = "Hello, world!"

# Save file contents to the specified file
file_manager.save_file(file_name, file_contents)

# Load file contents from the specified file
loaded_contents = file_manager.load_file(file_name)
```

### Reading and Writing Files

You can also directly read from and write content to files using the read_file and write_file methods:

```python
file_name = "example.txt"
file_contents = "Hello, world!"

# Write contents to the specified file
file_manager.write_file(file_name, file_contents)

# Read contents from the specified file
read_contents = file_manager.read_file(file_name)
```

### Handling File States

The FilesManager class keeps track of the state of each file that has been saved or loaded. You can check the state of a file using the get_file_state method:

```python
file_name = "example.txt"
state = file_manager.get_file_state(file_name)
print(f"File state for '{file_name}': {state}")
```

**Note:** The state is represented as a list of events. For example, if a file is saved and loaded, the state attribute (`file_manager.file_state[file_name]`) will be `["saved", "loaded"]`.

### Handling Exceptions

When loading a file, if the specified file is not found, the load_file method returns None and logs an error message using the logging module. To handle such cases, you can check if the loaded contents are None:

```python
file_name = "nonexistent_file.txt"
loaded_contents = file_manager.load_file(file_name)

if loaded_contents is None:
    print(f"The file '{file_name}' was not found.")
```



## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`centopy` was created by Vagner Bessa. Vagner Bessa retains all rights to the source and it may not be reproduced, distributed, or used to create derivative works.

## Credits

`centopy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
