import os
import pandas as pd
from typing import IO


def read_file_txt(file_path: str, splitter: str = '', encoding: str = 'utf-8'):
    file_pointer: IO = open(file_path, encoding=encoding)
    file_content: str = file_pointer.read()
    file_pointer.close()
    if len(splitter) > 0:
        file_content = file_content.split(splitter)
    return file_content

def read_file_xlsx(file_path: str):
    file_content = pd.read_excel(file_path, names=['Chapter', 'Verse', 'Meaning'])
    return file_content