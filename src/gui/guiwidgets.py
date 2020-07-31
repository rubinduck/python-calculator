"""
Module conating graphical parts of calculator GUI, without logic
"""

from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot
from PyQt5 import QtGui
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


class ErrorMessageWidget(QLabel):
	"""
	class represinting line with error message shown
	to user
	"""
	pass

class MainLineWidget(QLineEdit):
	"""
	Widget representing main line of calculator (line, where you enter your
	expressions and where you get the result)
	"""

	key_press_signal = pyqtSignal()

	def keyPressEvent(self,event):
		"""
		Method extending original keyPressEvent
		allows to copy all text in line if no text is selected
		"""
		self.key_press_signal.emit()
		if event.matches(QtGui.QKeySequence.Copy) and not self.hasSelectedText():
			QApplication.clipboard().setText(self.text())
			return
		super().keyPressEvent(event)


class GeneralControlButtonsPanel(QWidget):
	"""
	Class representing general case of control buttons grid
	"""
	SPACE_BETWEEN_BUTTONS = 5

	def __init__(self,*args,row_length,**kargs):
		super().__init__(*args,**kargs)

		self.row_length = row_length
		self.buttons = {}
		self.init_ui()

	def init_ui(self):
		self._layout = QGridLayout(self)
		self._layout.setSpacing(self.SPACE_BETWEEN_BUTTONS)


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

			self.add_button(label,row_number,column_number)
			column_number += 1

	def add_button(self,button_name:str,*position):
		"""
		Method adding buttons with labeled button_name, using 
		*position agruments to addWidget method of QLayout
		position: (row,column) or (row,column,rowSpan,columnSpan)
		"""
		button = QPushButton(self,text=button_name)
		button.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

		self.buttons[button_name] = button
		self._layout.addWidget(button,*position)


class MainControlButtonsWidget(GeneralControlButtonsPanel):
	"""
	Widget with main control buttons of calulator
	"""
	BUTTON_LABELS = ['7','8','9','(',')',
	                 '4','5','6','+','C',
	                 '1','2','3','-','',
	                 '0','.','/','*','']
	ENTER_CHAR_BUTTONS = ['0', '1', '2', '3', '4',
	                      '5', '6', '7', '8', '9',
	                      '(',')','.','+','-','/',
	                      "*"]

	enter_char = pyqtSignal(str)
	clear = pyqtSignal()
	carriage = pyqtSignal()

	def __init__(self,*args,**kargs):
		super().__init__(*args,row_length=5,**kargs)

		self.set_buttons(self.BUTTON_LABELS)
		self.add_button("⏎",2,4,2,1)
		self.set_up_signals()

	def set_up_signals(self):
		for button_name in self.buttons:
			if button_name in self.ENTER_CHAR_BUTTONS:
				self.buttons[button_name].clicked.connect(self._emit_enter_char)

		self.buttons["C"].clicked.connect(self._emit_clear)
		self.buttons["⏎"].clicked.connect(self._emit_carriage)


	@pyqtSlot()
	def _emit_enter_char(self):
		self.enter_char.emit(self.sender().text())

	@pyqtSlot()
	def _emit_clear(self):
		self.clear.emit()

	@pyqtSlot()
	def _emit_carriage(self):
		self.carriage.emit()

class CalculatorMainWindowGui(QMainWindow):
	"""
	Main window of calculator GUI
	Includes history widget, main line and control buttons panel
	"""

	MINIMUM_WIDTH = 200
	MINIMUM_HEIGHT = 300
	WIDGET_SPACING = 5

	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)
		self._widgets = {}
		self.init_ui()

	def init_ui(self):
		self.setMinimumSize(self.MINIMUM_WIDTH,self.MINIMUM_HEIGHT)

		self.add_content_container()
		self._layout.setSpacing(self.WIDGET_SPACING)

		content_container = self.content_container

		history_widget = HistoryWidget(content_container)
		eror_widget = ErrorMessageWidget()
		main_line_widget = MainLineWidget(content_container)
		main_controls_widget = MainControlButtonsWidget(content_container)

		self._widgets["history"] = history_widget
		self._widgets["error_message"] = eror_widget
		self._widgets["main_line"] = main_line_widget
		self._widgets["main_controls"] = main_controls_widget

		for widget in self._widgets.values():
			widget.setMinimumSize(0,0)
			self._layout.addWidget(widget)

		eror_widget.hide()

	def add_content_container(self):
		"""
		Method creating container for all other widgets and VBOX layout for it
		"""
		self.content_container = QWidget(self)
		self.setCentralWidget(self.content_container)

		self._layout = QVBoxLayout(self.content_container)
		self.content_container.setLayout(self._layout)
