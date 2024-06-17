import os
from ujson import loads, dump
import aiofiles

async def get_json(filename: str):
    path = f"data/{filename}"
    if os.path.exists(path):
        async with aiofiles.open(path,'r', encoding='utf-8') as file:
            return loads(await file.read())
    return {}

def load_json(filename, item):
    path = f'data/{filename}'
    with open(path, 'w', encoding='utf-8') as file:
        dump(item, file, indent=4, ensure_ascii=False)