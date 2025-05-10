import os

project_name = "."  # current directory

folders = [
    "data/raw",
    "data/processed",
    "notebooks",
    "scripts",
    "models",
    "reports/figures",
    "src",
    "src/components",
    "src/utils",
    "src/pipelines",
    "src/config",
    "tests"
]

files = [
    "README.md",
    "requirements.txt",
    "setup.py",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/utils/__init__.py",
    "src/pipelines/__init__.py",
    "src/config/__init__.py",
    "tests/__init__.py"
]

for folder in folders:
    os.makedirs(os.path.join(project_name, folder), exist_ok=True)

for file in files:
    file_path = os.path.join(project_name, file)
    with open(file_path, 'w') as f:
        pass

print("Project structure created successfully in current directory!")
