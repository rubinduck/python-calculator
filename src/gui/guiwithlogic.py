"""
Module conating unification of GUI and it's logic
"""

from PyQt5.QtCore import Qt, pyqtSlot

from .guiwidgets import CalculatorMainWindowGui

from core import (settings, AngleType, calculate_expression, format_decimal,
                  IncorrectInputError)


class CalculatorMainWindow(CalculatorMainWindowGui):
    """
    Class uniting GUI sceleton with logic
    """
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.init_logic()

    def init_logic(self):
        self.setup_input_focus()
        self.setup_calculation_logic()
        self.setup_buttons_work()
        self.setup_settings_work()

    def setup_input_focus(self):
        """
        Method creating behavior,where keyboard inputs goes to main line widget
        of calculator
        """
        main_line_widget = self._widgets["main_line"]
        main_line_widget.setFocus(Qt.OtherFocusReason)

        for widget in self._widgets.values():
            if widget != main_line_widget:
                pass
                widget.setFocusProxy(main_line_widget)
                widget.setFocusPolicy(Qt.NoFocus)

        for widget in self._widgets["main_controls"].buttons.values():
            widget.setFocusPolicy(Qt.NoFocus)

    def setup_calculation_logic(self):
        self._widgets["main_line"].returnPressed.connect(self.calculate)

    def setup_buttons_work(self):
        """method connecting buttons signals to slots"""
        main_controls = self._widgets["main_controls"]
        main_controls.enter_char.connect(self.enter_char)
        main_controls.clear.connect(self.clear)
        main_controls.carriage.connect(self.calculate)

    @pyqtSlot(str)
    def enter_char(self, value: str):
        """slot adding char to main line"""
        main_line = self._widgets["main_line"]
        main_line.setText(main_line.text() + value)

    @pyqtSlot()
    def clear(self):
        self._widgets["main_line"].setText('')

    @pyqtSlot()
    def calculate(self, *args, **kargs):
        """
        slot extracting expression from main line, evaluating it and
        displaing results
        """
        expression = self._widgets["main_line"].text()
        try:
            result = calculate_expression(expression)
        except IncorrectInputError as ex:
            self.show_error_message(ex)
            return

        result = format_decimal(result)
        self._widgets["history"].add_line(f"{expression}={result}")
        self._widgets["main_line"].setText(f"{result}")

    def setup_settings_work(self):
        """
        method setting up slots changing calculator settings
        """
        menu = self._widgets["menu"]
        menu.angle_type_changed.connect(self.angle_type_changed)
        menu.accuracy_changed.connect(self.accuracy_changed)

    @pyqtSlot(str)
    def angle_type_changed(self, value):
        if value == "radian":
            settings.set_angle_type(AngleType.RADIAN)
        elif value == "degree":
            settings.set_angle_type(AngleType.DEGREE)
        else:
            raise Exception("Something messed up with settings")

    @pyqtSlot(int)
    def accuracy_changed(self, value):
        settings.set_accuracy(value)

    def show_error_message(self, ex: Exception):
        """
        method for displaying error message and adding slots to hide it after
        key or button is pressed
        """
        text = ex.args[0]
        error_widget = self._widgets["error_message"]
        error_widget.setText(text)
        error_widget.show()

        self._widgets["main_line"].key_press_signal.connect(self.hide_error_message)
        self._widgets["main_controls"].enter_char.connect(self.hide_error_message)
        self._widgets["main_controls"].clear.connect(self.hide_error_message)

    @pyqtSlot()
    def hide_error_message(self):
        """method hiding error widget and disconecting itself from input slots"""
        self._widgets["error_message"].hide()
        self._widgets["main_line"].key_press_signal.disconnect(self.hide_error_message)
        self._widgets["main_controls"].enter_char.disconnect(self.hide_error_message)
        self._widgets["main_controls"].clear.disconnect(self.hide_error_message)