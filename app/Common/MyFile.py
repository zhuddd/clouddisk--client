import atexit
from uuid import uuid1
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal

from app.Common import _dic_


class CheckFile(QThread):
    """
    检查文件
    hashes: (file_hash, check_hash)
    """
    hashes = pyqtSignal(tuple)

    def __init__(self, path, *args, **kwargs):
        super(CheckFile, self).__init__(*args, **kwargs)
        self.path = path
        atexit.register(self.terminate)

    def run(self):
        data=get_file_hash(self.path)
        self.hashes.emit(data)



def create_tree(path)->(dict,dict):
    """
    创建文件树
    :param path: 文件路径
    :return: (tree,path_list)
    """
    try:
        path = Path(path)
    except:
        return None, None
    uid = uuid1().hex
    tmp_tree = {"uid": uid,
                "name": path.name,
                "type": get_file_type(str(path)),
                "size": path.stat().st_size,
                "children": []}
    tmp_path = {}
    if path.is_file():
        tmp_path[uid] = str(path)
    if path.is_dir():
        tmp_tree["size"] = 0
        for file in path.iterdir():
            new_tree, new_path = create_tree(str(file))
            if new_tree is not None:
                tmp_tree["children"].append(new_tree)
                tmp_path.update(new_path)

    return tmp_tree, tmp_path


def get_all_file(path):
    """
    获取所有文件
    :param path: 文件路径
    :return: 所有文件
    """
    try:
        path = Path(path)
    except:
        return None
    if path.is_dir():
        r = []
        for file in path.iterdir():
            item = get_all_file(str(file))
            if item is not None:
                r.extend(item)
        return r
    else:
        return [str(path)]


def get_file_type(path: str) -> str:
    """
    获取文件类型
    :param path: 文件路径
    :return: 文件类型
    """

    def get_(path: str) -> str:
        path = Path(path)
        if path.is_dir():
            return "folder"
        if path.is_file():
            file_extension = path.suffix  # 分离文件扩展名
            return file_extension[1:].lower() if file_extension else "unknown"
        return "unknown"

    return _dic_._dic.get(get_(path), "default")


def get_file_hash(path, key=""):
    """
    获取文件的md5值和使用md5值再次计算出的md5值
    :param path: 文件路径
    :param key: md5值的key
    :return: file_hash和check_hash的元组
    """
    if not Path(path).is_file():
        return "0", "0"
    import hashlib
    s = hashlib.sha256(key.encode())
    with open(path, 'rb') as f:
        while True:
            data = f.readline()
            if not data:
                break
            s.update(data)
    file_hash = s.hexdigest()
    s.update(file_hash.encode())
    check_hash = s.hexdigest()

    return file_hash, check_hash


def get_file_hash_file(file, key=""):
    """
    获取文件的md5值
    :param file: 文件
    :param key: md5值的key
    :return: md5值
    """
    import hashlib
    m = hashlib.sha256(key.encode())
    m.update(file)
    return m.hexdigest()


def convert_size(size_bytes):
    """
    转换文件大小
    :param size_bytes:
    :return:
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size_bytes > 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024
        unit_index += 1
    return round(size_bytes, 2), units[unit_index]
