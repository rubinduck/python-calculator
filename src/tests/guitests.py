if __name__ == "__main__":
	import sys, os
	dirname=os.path.dirname
	path = dirname(dirname(__file__))
	sys.path.append(path)

from PyQt5.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QWidget

import gui


class WidgetTestingContainer(QMainWindow):
	def __init__(self,size:"(x,y,w,h)",WidgetClass,*args,widget_args=(),**kargs):
		super().__init__(*args,**kargs)
		self.setGeometry(*size)
		self.place_widget(WidgetClass,widget_args)
		self.init_ui()
		self.show()

	def place_widget(self,WidgetClass,widget_args):
		self.content_container = QWidget(self)
		self.setCentralWidget(self.content_container)

		layout = QVBoxLayout(self.content_container)
		self.content_container.setLayout(layout)

		widget = WidgetClass(*widget_args,self.content_container)
		self._widget = widget
		layout.addWidget(widget)

	def init_ui(self):
		pass

def test_HistoryWidget():
	HistoryWidget = gui.HistoryWidget

	class Main(WidgetTestingContainer):
		def init_ui(self):
			widget = self._widget
			widget.setText("fffffffffffffffffffffff\n" * 60)
			widget.add_line("test")
			widget.add_line("one more test")
			widget.resize(150,150)	

	run_test_app(Main,(200,200,200,200),HistoryWidget)

def test_MainLineWidget():
	MainLineWidget = gui.MainLineWidget
	run_test_app(WidgetTestingContainer,(200,200,400,50),MainLineWidget)

def test_GeneralControlButtonsPanel():

	GeneralControlButtonsPanel = gui.GeneralControlButtonsPanel
	class Main(WidgetTestingContainer):
		def init_ui(self):
			self._widget.set_buttons(["+","-","*"])

	run_test_app(Main,(200,200,200,200),GeneralControlButtonsPanel,widget_args=(2,))


def run_test_app(MainWindowClass,*args,widget_args=()):
	app = QApplication([])
	window = MainWindowClass(*args,widget_args=widget_args)
	window.show()
	app.exec()

def run_gui_tests():
	test_HistoryWidget()
	test_MainLineWidget()
	test_GeneralControlButtonsPanel()

if __name__ == "__main__":
	run_gui_tests()