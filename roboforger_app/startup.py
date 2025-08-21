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


import os
import sys
import multiprocessing
import logging


class StartUp:
    """Necessary steps for environment, Python and Qt"""

    @staticmethod
    def configure_qt_application_data():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationName("RoboForger")
        QCoreApplication.setOrganizationName("JuSo")
        QCoreApplication.setApplicationVersion("0.0.1a")

    @staticmethod
    def configure_environment_variables():
        # Qt expects "qtquickcontrols2.conf" at root level, but the way we handle resources does not allow that.
        # So we need to override the path here
        os.environ["QT_QUICK_CONTROLS_CONF"] = ":/data/qtquickcontrols2.conf"

    @staticmethod
    def import_resources():
        import roboforger_app.generated_resources  # noqa: F401

    @staticmethod
    def import_bindings():
        import roboforger_app.pyobjects  # noqa: F401
        import roboforger_app.pyobjects.geometries

    @staticmethod
    def start_application(debug: bool = False):
        from roboforger_app.application import RoboforgerApp
        app = RoboforgerApp(sys.argv)

        app.set_window_icon()
        app.set_up_signals()
        app.set_up_window_event_filter()
        app.start_engine(debug=debug)
        app.set_up_window_effects()
        app.verify()

        sys.exit(app.exec())


def perform_startup(debug: bool = False):
    multiprocessing.freeze_support()

    we = StartUp()

    we.configure_qt_application_data()
    we.configure_environment_variables()

    we.import_resources()
    we.import_bindings()

    we.start_application(debug=debug)