from PySide6.QtWidgets import QApplication
from aaf_display import MainWindow
import sys

app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

# Start the event loop
app.exec()
