from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel,QApplication,QScrollArea,QWidget,QVBoxLayout,QMainWindow

class ScrollableLable (QScrollArea):
	"""
	Wrapper around QLabel class, that enables it to be scrollable
	Passes all undefined in QScrollabel argument calls to label obj inside
	"""
	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)

		self.setWidgetResizable(True)

		content_container = QWidget(self)
		layout = QVBoxLayout(content_container)
		self.label = QLabel(content_container)

		layout.addWidget(self.label)
		content_container.setLayout(layout)
		self.setWidget(content_container)

	def __getattr__(self,name):
		return getattr(self.label,name)

class HistoryWidget(ScrollableLable):
	"""
	Extension of ScrollableLable class, representing History Widget
	New content is added line by line
	"""
	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)

	def set_text(self,text):
		self.setText(text)

	def add_line(self,new_line):
		new_text = self.text() + "\n" + new_line
		self.set_text(new_text)





if __name__ == "__main__":
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

	app = QApplication([])
	window = Main()
	window.show()
	app.exec()
