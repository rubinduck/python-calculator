if __name__ == "__main__":
	import sys, os
	dirname=os.path.dirname
	path = dirname(dirname(__file__))
	sys.path.append(path)

from PyQt5.QtWidgets import QApplication,QMainWindow


import gui

def test_HistoryWidget():
	HistoryWidget = gui.HistoryWidget

	class Main(QMainWindow):
		"""
		test class for HistoryWidgetFunctionality
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

def run_test_app(MainWindowClass):
	app = QApplication([])
	window = MainWindowClass()
	window.show()
	app.exec()

def run_gui_tests():
	test_HistoryWidget()

if __name__ == "__main__":
	run_gui_tests()