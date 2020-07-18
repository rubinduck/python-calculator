if __name__ == "__main__":
	import sys, os
	dirname=os.path.dirname
	path = dirname(dirname(__file__))
	sys.path.append(path)

from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QWidget

import gui

def test_HistoryWidget():
	HistoryWidget = gui.HistoryWidget

	class Main(QMainWindow):
		"""
		test class for HistoryWidget
		"""
		def __init__(self):
			super().__init__()
			self.setGeometry(200,200,500,400)
			self.init_ui()
			self.show()

		def init_ui(self):
			label = HistoryWidget(self)

			label.setText("fffffffffffffffffffffff\n" * 15)
			label.add_line("test")
			label.add_line("one more test")

			label.setGeometry(100, 100, 300, 150)

	run_test_app(Main)

def test_MainLineWidget():

	MainLineWidget = gui.MainLineWidget
	class Main(QMainWindow):
		"""
		test class for MainLineWidget
		"""
		def __init__(self):
			super().__init__()
			self.setGeometry(200,200,400,50)
			self.init_ui()
			self.show()

		def init_ui(self):
			self.content_container = QWidget(self)
			self.setCentralWidget(self.content_container)

			layout = QVBoxLayout(self.content_container)
			self.content_container.setLayout(layout)

			widget = MainLineWidget(self.content_container)
			layout.addWidget(widget)

	run_test_app(Main)

def test_GeneralControlButtonsPanel():

	GeneralControlButtonsPanel = gui.GeneralControlButtonsPanel
	class Main(QMainWindow):
		"""
		test class for GeneralControlButtonsPanel
		"""
		def __init__(self):
			super().__init__()
			self.setGeometry(200,200,200,200)
			self.init_ui()
			self.show()

		def init_ui(self):
			self.content_container = QWidget(self)
			self.setCentralWidget(self.content_container)

			layout = QVBoxLayout(self.content_container)
			self.content_container.setLayout(layout)

			widget = GeneralControlButtonsPanel(2,self.content_container)
			layout.addWidget(widget)

			widget.set_buttons(["+","-","*"])

	run_test_app(Main)


def run_test_app(MainWindowClass):
	app = QApplication([])
	window = MainWindowClass()
	window.show()
	app.exec()

def run_gui_tests():
	test_HistoryWidget()
	test_MainLineWidget()
	test_GeneralControlButtonsPanel()

if __name__ == "__main__":
	run_gui_tests()