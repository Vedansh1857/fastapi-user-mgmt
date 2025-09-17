import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "mlProject"

list_of_files = [
    f"app/api/__init__.py",
    f"app/core/__init__.py",
    f"app/db/__init__.py",
    f"app/models/__init__.py",
    f"app/services/__init__.py",
    f"app/repositories/__init__.py",
    f"app/schemas/__init__.py",
    f"app/main.py",
    "requirements.txt",
    "alembic.ini",
    ".env",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")