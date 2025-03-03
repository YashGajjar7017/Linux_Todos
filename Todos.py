import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox, QLabel
from PyQt6.QtGui import QPalette, QLinearGradient, QBrush, QColor, QFont
from PyQt6.QtCore import Qt

TODO_FILE = os.path.expanduser("~/.todo_list")

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        file.write("\n".join(tasks) + "\n")

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("🔥 Ultra Stylish To-Do List 🔥")
        self.setGeometry(100, 100, 550, 450)
        
        # Apply Gradient Background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#ff416c"))  # Hot Pink
        gradient.setColorAt(0.5, QColor("#ff4b2b"))  # Reddish-Orange
        gradient.setColorAt(1.0, QColor("#ff9a9e"))  # Soft Pink
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
        
        self.layout = QVBoxLayout()
        
        # Header Label
        self.header = QLabel("🔥 My Super Cool To-Do List 🔥")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.header.setStyleSheet("color: white; padding: 12px; background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        self.layout.addWidget(self.header)
        
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background: rgba(255, 255, 255, 0.9); border-radius: 10px; font-size: 14px; padding: 5px;")
        self.layout.addWidget(self.task_list)
        
        button_style = "border: none; padding: 12px; font-size: 14px; color: white; font-weight: bold; border-radius: 8px;"
        
        self.add_button = QPushButton("➕ Add Task")
        self.add_button.setStyleSheet(button_style + "background: linear-gradient(to right, #ff416c, #ff4b2b);")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)
        
        self.complete_button = QPushButton("✔ Complete Task")
        self.complete_button.setStyleSheet(button_style + "background: linear-gradient(to right, #56ab2f, #a8e063);")
        self.complete_button.clicked.connect(self.complete_task)
        self.layout.addWidget(self.complete_button)
        
        self.delete_button = QPushButton("🗑 Delete Task")
        self.delete_button.setStyleSheet(button_style + "background: linear-gradient(to right, #c471ed, #f64f59);")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)
        self.load_tasks()
    
    def load_tasks(self):
        self.task_list.clear()
        tasks = load_tasks()
        self.task_list.addItems(tasks)
    
    def add_task(self):
        task, ok = QInputDialog.getText(self, "New Task", "Enter task:")
        if ok and task:
            tasks = load_tasks()
            tasks.append(task)
            save_tasks(tasks)
            self.load_tasks()
    
    def complete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            tasks = load_tasks()
            tasks.pop(selected_task)
            save_tasks(tasks)
            self.load_tasks()
            QMessageBox.information(self, "Task Completed", "🔥 Task marked as completed! 🔥")
        else:
            QMessageBox.warning(self, "Error", "No task selected.")
    
    def delete_task(self):
        selected_task = self.task_list.currentRow()
        if selected_task >= 0:
            tasks = load_tasks()
            tasks.pop(selected_task)
            save_tasks(tasks)
            self.load_tasks()
            QMessageBox.information(self, "Task Deleted", "🗑 Task removed successfully!")
        else:
            QMessageBox.warning(self, "Error", "No task selected.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
