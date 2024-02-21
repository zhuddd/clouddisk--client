import win32file
import win32pipe
from PyQt5.QtCore import QThread, pyqtSignal


class PipeMsg(QThread):
    msg=pyqtSignal(str)

    def __init__(self, parent=None):
        super(PipeMsg, self).__init__(parent)

    def run(self):
        self.start_server()

    def create_named_pipe(self):
        pipe_name = r'\\.\pipe\cloud'
        pipe = win32pipe.CreateNamedPipe(
            pipe_name,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            win32pipe.PIPE_UNLIMITED_INSTANCES,
            65536,
            65536,
            0,
            None
        )
        return pipe

    def start_server(self):
        while True:
            pipe = self.create_named_pipe()
            win32pipe.ConnectNamedPipe(pipe, None)
            data = self.read_from_pipe(pipe)
            self.msg.emit(data)

    def read_from_pipe(self,pipe):
        buffer_size = 1024
        data = win32file.ReadFile(pipe, buffer_size)[1].decode('utf-8')
        return data