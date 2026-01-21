# Copyright
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import platform
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon


class RoboforgerApp(QApplication):

    def __init__(self, args):
        super().__init__(args)

        self._event_filter = None
        self._effects = None
    
    def set_window_icon(self):
        icon = QIcon(":/data/icon.ico")
        self.setWindowIcon(icon)

    def set_up_window_event_filter(self):
        if platform.system() == "Windows":
            from roboforger_app.framelesswindow.win import WindowsEventFilter
            self._event_filter = WindowsEventFilter(border_width=5)
            self.installNativeEventFilter(self._event_filter)
        elif platform.system() == "Linux":
            from roboforger_app.framelesswindow.linux import LinuxEventFilter
            self._event_filter = LinuxEventFilter(border_width=5)
            self.installEventFilter(self._event_filter)

    def set_up_window_effects(self):
        if sys.platform == "win32":

            # if not self.topLevelWindows():
                
            #     raise RuntimeError("No top level windows found to apply effects.")

            # hwnd = self.topLevelWindows()[0].winId()

            # from roboforger_app.framelesswindow.win import WindowsWindowEffect
            # self._effects = WindowsWindowEffect()
            # self._effects.addShadowEffect(hwnd)
            # self._effects.addWindowAnimation(hwnd)
            pass

    def verify(self):
        pass
