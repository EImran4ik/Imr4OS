import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QSplashScreen, QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

class WindowsOS(QWidget):
    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()

        self.commands = {
            "dir": self.list_directory,
            "cd": self.change_directory,
            "create": self.create_file,
            "rename": self.rename_file,
            "delete": self.delete_file,
            "paint": self.open_paint,
            "notepad": self.open_notepad,
            "exit": self.exit_system
        }

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Windows 3.0 Command Prompt')

        self.label_prompt = QLabel('Microsoft Windows 3.0 Command Prompt')
        self.label_current_dir = QLabel('Current Directory: ' + self.current_directory)
        self.text_output = QTextEdit()
        self.text_input = QLineEdit()
        self.btn_submit = QPushButton('Submit')

        self.btn_paint = QPushButton('Paint')
        self.btn_paint.clicked.connect(self.open_paint)
        self.btn_notepad = QPushButton('Notepad')
        self.btn_notepad.clicked.connect(self.open_notepad)

        layout = QVBoxLayout()
        layout.addWidget(self.label_prompt)
        layout.addWidget(self.label_current_dir)
        layout.addWidget(self.text_output)
        layout.addWidget(self.text_input)
        layout.addWidget(self.btn_submit)
        layout.addWidget(self.btn_paint)
        layout.addWidget(self.btn_notepad)
        self.setLayout(layout)

        self.btn_submit.clicked.connect(self.process_command)

    def process_command(self):
        command_input = self.text_input.text().strip()
        self.text_input.clear()

        parts = command_input.split(" ")
        command = parts[0]
        args = parts[1:]

        if command in self.commands:
            output = self.commands[command](args)
            self.text_output.append(output)
        else:
            self.text_output.append("Command not found")

    def list_directory(self, args):
        files = os.listdir(self.current_directory)
        output = "Files in directory:\n"
        for file in files:
            output += file + '\n'
        return output

    def change_directory(self, args):
        if len(args) == 0:
            return "Usage: cd [directory]"
        else:
            new_directory = args[0]
            if os.path.isdir(new_directory):
                os.chdir(new_directory)
                self.current_directory = os.getcwd()
                self.label_current_dir.setText('Current Directory: ' + self.current_directory)
            else:
                return "Directory not found"

    def create_file(self, args):
        if len(args) == 0:
            return "Usage: create [filename]"
        else:
            filename = args[0]
            with open(os.path.join(self.current_directory, filename), 'w') as f:
                pass
            return f"File {filename} created"

    def rename_file(self, args):
        if len(args) != 2:
            return "Usage: rename [old_name] [new_name]"
        else:
            old_name, new_name = args
            try:
                os.rename(os.path.join(self.current_directory, old_name), os.path.join(self.current_directory, new_name))
                return f"File {old_name} renamed to {new_name}"
            except FileNotFoundError:
                return "File not found"

    def delete_file(self, args):
        if len(args) == 0:
            return "Usage: delete [filename]"
        else:
            filename = args[0]
            try:
                os.remove(os.path.join(self.current_directory, filename))
                return f"File {filename} deleted"
            except FileNotFoundError:
                return "File not found"

    def open_paint(self, args):
        os.system("mspaint")  # Открыть Paint

    def open_notepad(self, args):
        os.system("notepad")  # Открыть блокнот

    def exit_system(self, args):
        self.close()

class BootScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap("windows_logo.png")  # Замените "windows_logo.png" на путь к вашему изображению загрузочного экрана
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setMask(pixmap.mask())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    boot_screen = BootScreen()
    boot_screen.show()

    QTimer.singleShot(3000, boot_screen.close)  # Закрываем загрузочный экран через 3 секунды

    window = WindowsOS()
    window.show()

    sys.exit(app.exec_())
