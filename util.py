from typing import Union
from pathlib import Path

def get_module_in_dir(folder: Union[Path, str]):
    """一个简单获取文件夹内所有模组的函数"""
    module_dir = Path(folder) if isinstance(folder, str) else folder
    parents_name = ".".join(module_dir.parts)
    for path in module_dir.iterdir():
        if any((path.name.startswith('_'),
          path.is_file() and path.suffix != '.py',
          path.is_dir() and not (path / '__init__.py').exists())):
            continue
        yield f'{parents_name}.{path.stem}'