class File:
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
        self.icon = data.get('icon')
        self.size = data.get('size')

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