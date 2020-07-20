from PyQt5.QtCore import Qt

from .guiwidgets import CalculatorMainWindowGui

class CalculatorMainWindow(CalculatorMainWindowGui):
	"""
	Class uniting GUI sceleton with logic
	"""
	def __init__(self,*args,**kargs):
		super().__init__(*args,**kargs)
		self.init_logic()

	def init_logic(self):
		self.set_input_focus()

	def set_input_focus(self):
		main_line_widget = self._widgets["main_line"]
		main_line_widget.setFocus(Qt.OtherFocusReason)

		for widget in self._widgets.values():
			if widget != main_line_widget:
				pass
				widget.setFocusProxy(main_line_widget)
				widget.setFocusPolicy(Qt.NoFocus)

		for widget in self._widgets["main_controls"].buttons:
			widget.setFocusProxy(main_line_widget)
			widget.setFocusPolicy(Qt.NoFocus)

