from app.Common.MyIcon import MyIcon


class File:
    """
    文件类，用于存储文件信息
    """

    def __init__(self, data):
        self.id = data.get('Id')
        self.name = data.get('file_name')
        self.type = data.get('file_type')
        self.user = data.get('user_id')
        self.parent = data.get('parent_folder')
        self.folder = data.get('is_folder')
        self.delete = data.get('is_delete')
        self.face = data.get('file_face')
        self.time = data.get('upload_time')
        self.icon = data.get('icon')  # type:MyIcon
        self.size = data.get('size')
        self.fid = data.get('fid')

    def __str__(self):
        return (f"File: {self.name} "
                f"Type: {self.type} "
                f"User: {self.user} "
                f"Parent: {self.parent} "
                f"Folder: {self.folder} "
                f"Delete: {self.delete} "
                f"Face: {self.face} "
                f"Time: {self.time} "
                f"Icon: {self.icon} "
                f"Size: {self.size} ")
