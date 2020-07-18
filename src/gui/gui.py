from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel,QApplication,QScrollArea,QPushButton,
QWidget,QVBoxLayout,QMainWindow,QLineEdit,QGridLayout,QSizePolicy)

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



class MainLineWidget(QLineEdit):
	"""
	Widget representing main line of calculator (line, where you enter your
	expressions and where you get the result)
	"""

class GeneralControlButtonsPanel(QWidget):
	"""
	Class representing general case of control buttons grid
	"""
	SPACE_BETWEEN_BUTTONS = 5

	def __init__(self,row_length,*args,**kargs):
		super().__init__(*args,**kargs)

		self.row_length = row_length
		self.buttons = []
		self.init_ui()

	def init_ui(self):
		self.__layout = QGridLayout(self)
		self.__layout.setSpacing(self.SPACE_BETWEEN_BUTTONS)


	def set_buttons(self,button_labels:list):
		"""
		Method sets buttons with passed labels to widget's grid,
		in accordance with row_length.
		New grid will be row_length x len(button_list)/row_length sized
		"""

		row_number = 0
		column_number = 0
		for label in button_labels:
			if column_number == self.row_length:
				column_number = 0
				row_number += 1

			button = QPushButton(self,text=label)
			button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

			self.buttons.append(button)
			self.__layout.addWidget(button,row_number,column_number)
			column_number += 1
