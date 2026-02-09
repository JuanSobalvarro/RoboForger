from PySide6.QtWidgets import (
    QWidget, 
    QFrame, 
    QHBoxLayout, 
    QVBoxLayout, 
    QLabel, 
    QLayout,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QScrollArea,
)
from PySide6.QtCore import (
    Signal,
    SignalInstance,
)

from RoboForger.app.components.field import Field, LabelPosition, LabelAnchor
from RoboForger.app.components.separator import LineSeparator
from RoboForger.app.components.label import Label, LabelTag
from RoboForger.app.utils import make_scrollable
from RoboForger.app.preview.drawing.parameters import ProcessingParameters

from typing import Any


def safe_emit_value(signal: SignalInstance, value: Any, cast_type: type):
    try:
        casted_value = cast_type(value)
        signal.emit(casted_value)
    except ValueError:
        pass

class LeftPanel(QFrame):
    
    on_scale_factor_changed = Signal(float)
    on_float_precision_changed = Signal(int)
    on_polyline_velocity_changed = Signal(float)
    on_arc_velocity_changed = Signal(float)
    on_circle_velocity_changed = Signal(float)
    on_lifting_height_changed = Signal(float)
    on_auto_trace_changed = Signal(bool)
    on_offset_programming_changed = Signal(bool)

    def __init__(self):
        super().__init__()

        self.scale_factor_field: Field
        self.float_precision_field: Field
        self.polyline_vel_field: Field
        self.arc_vel_field: Field
        self.circle_velocity_field: Field
        self.lifting_height_field: Field
        self.auto_trace_field: Field
        self.offset_programming_field: Field

        self.setup_ui()

        self.connect_signals()

    def setup_ui(self):
        layout: QLayout = QVBoxLayout(self)

        # Title label
        title_label = Label("Robo Parameters", self, tag=LabelTag.HEADER)
        layout.addWidget(title_label)

        # parser section
        parser_label = Label("Parser", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(parser_label)

        self.scale_factor_field = Field("Scale Factor", QLineEdit(), 1.0, LabelPosition.LEFT)
        layout.addWidget(self.scale_factor_field)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # converter section
        converter_label = Label("Converter", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(converter_label)

        self.float_precision_field = Field("Float Precision", QLineEdit(), 4, LabelPosition.LEFT)
        layout.addWidget(self.float_precision_field)

        self.polyline_vel_field = Field("Polyline Velocity", QLineEdit(), 500.0, LabelPosition.LEFT)
        layout.addWidget(self.polyline_vel_field)

        self.arc_vel_field = Field("Arc Velocity", QLineEdit(), 500.0, LabelPosition.LEFT)
        layout.addWidget(self.arc_vel_field)

        self.circle_velocity_field = Field("Circle Velocity", QLineEdit(), 500.0, LabelPosition.LEFT)
        layout.addWidget(self.circle_velocity_field)

        self.lifting_height_field = Field("Lifting Height", QLineEdit(), 50.0, LabelPosition.LEFT)
        layout.addWidget(self.lifting_height_field)

        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # Drawing section
        drawing_label = Label("Drawing and Rapid", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(drawing_label)

        self.auto_trace_field = Field("Use auto trace detection", QCheckBox(), True, LabelPosition.RIGHT, LabelAnchor.LEFT)
        layout.addWidget(self.auto_trace_field)

        self.offset_programming_field = Field("Use Offset Programming", QCheckBox(), True, LabelPosition.RIGHT, LabelAnchor.LEFT)
        layout.addWidget(self.offset_programming_field)

        self.setLayout(layout)

    def connect_signals(self):
        self.scale_factor_field.value_changed.connect(lambda v: safe_emit_value(self.on_scale_factor_changed, v, float))
        self.float_precision_field.value_changed.connect(lambda v: safe_emit_value(self.on_float_precision_changed, v, int))
        self.polyline_vel_field.value_changed.connect(lambda v: safe_emit_value(self.on_polyline_velocity_changed, v, float))
        self.arc_vel_field.value_changed.connect(lambda v: safe_emit_value(self.on_arc_velocity_changed, v, float))
        self.circle_velocity_field.value_changed.connect(lambda v: safe_emit_value(self.on_circle_velocity_changed, v, float))
        self.lifting_height_field.value_changed.connect(lambda v: safe_emit_value(self.on_lifting_height_changed, v, float))
        self.auto_trace_field.value_changed.connect(lambda v: safe_emit_value(self.on_auto_trace_changed, v, bool))
        self.offset_programming_field.value_changed.connect(lambda v: safe_emit_value(self.on_offset_programming_changed, v, bool))        


class RightPanel(QFrame):
    on_tool_name_changed = Signal(str)

    on_inferior_limit_x_changed = Signal(float)
    on_inferior_limit_y_changed = Signal(float)
    on_inferior_limit_z_changed = Signal(float)

    on_superior_limit_x_changed = Signal(float)
    on_superior_limit_y_changed = Signal(float)
    on_superior_limit_z_changed = Signal(float)

    on_origin_x_changed = Signal(float)
    on_origin_y_changed = Signal(float)
    on_origin_z_changed = Signal(float)

    on_zero_x_changed = Signal(float)
    on_zero_y_changed = Signal(float)
    on_zero_z_changed = Signal(float)

    on_load_dxf_clicked = Signal()
    on_process_clicked = Signal()
    on_save_rapid_clicked = Signal()

    def __init__(self):
        super().__init__()

        self.tool_field: Field

        self.inferior_limit_x_field: Field
        self.inferior_limit_y_field: Field
        self.inferior_limit_z_field: Field

        self.superior_limit_x_field: Field
        self.superior_limit_y_field: Field
        self.superior_limit_z_field: Field

        self.origin_x_field: Field
        self.origin_y_field: Field
        self.origin_z_field: Field

        self.zero_x_field: Field
        self.zero_y_field: Field
        self.zero_z_field: Field

        self.load_button: QPushButton
        self.process_button: QPushButton
        self.save_button: QPushButton

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout: QLayout = QVBoxLayout(self)

        # Title label
        # title_label = Label("Coords Parameters", self, tag=LabelTag.HEADER)
        # layout.addWidget(title_label)

        # tool section
        tool_label = Label("Tool", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(tool_label)

        self.tool_field = Field("Tool name", QLineEdit(), "tool0", LabelPosition.LEFT)
        layout.addWidget(self.tool_field)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # workspace limits
        # TODO: implement a small square showing the limit vectors visually
        workspace_label = Label("Workspace Limits InfLeft - SupRight", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(workspace_label)

        vectors_layout = QHBoxLayout()
        
        inf_left_layout = QVBoxLayout()

        self.inferior_limit_x_field = Field("X", QLineEdit(), -300.0, LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_x_field)

        self.inferior_limit_y_field = Field("Y", QLineEdit(), -300.0, LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_y_field)

        self.inferior_limit_z_field = Field("Z", QLineEdit(), -100.0, LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_z_field)

        sup_right_layout = QVBoxLayout()

        self.superior_limit_x_field = Field("X", QLineEdit(), 800.0, LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_x_field)

        self.superior_limit_y_field = Field("Y", QLineEdit(), 800.0, LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_y_field)

        self.superior_limit_z_field = Field("Z", QLineEdit(), 800.0, LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_z_field)

        vectors_layout.addLayout(inf_left_layout)
        vectors_layout.addLayout(sup_right_layout)

        layout.addLayout(vectors_layout)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # References section
        references_label = Label("References", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(references_label)

        references_layout = QHBoxLayout()

        origin_layout = QVBoxLayout()

        self.origin_x_field = Field("Origin X", QLineEdit(), 450.0, LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_x_field)

        self.origin_y_field = Field("Origin Y", QLineEdit(), 450.0, LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_y_field)

        self.origin_z_field = Field("Origin Z", QLineEdit(), 0.0, LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_z_field)

        zero_layout = QVBoxLayout()

        self.zero_x_field = Field("Zero X", QLineEdit(), 0.0, LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_x_field)

        self.zero_y_field = Field("Zero Y", QLineEdit(), 0.0, LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_y_field)

        self.zero_z_field = Field("Zero Z", QLineEdit(), 0.0, LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_z_field)

        references_layout.addLayout(origin_layout)
        references_layout.addLayout(zero_layout)
        layout.addLayout(references_layout)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # Processing section
        # temporal buttons since we should use custom ones with icons later
        self.load_button = QPushButton("Load DXF", self)
        self.process_button = QPushButton("Process", self)
        self.save_button = QPushButton("Save RAPID", self)
        layout.addWidget(self.load_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def connect_signals(self):
        self.tool_field.value_changed.connect(lambda v: safe_emit_value(self.on_tool_name_changed, v, str))

        self.inferior_limit_x_field.value_changed.connect(lambda v: safe_emit_value(self.on_inferior_limit_x_changed, v, float))
        self.inferior_limit_y_field.value_changed.connect(lambda v: safe_emit_value(self.on_inferior_limit_y_changed, v, float))
        self.inferior_limit_z_field.value_changed.connect(lambda v: safe_emit_value(self.on_inferior_limit_z_changed, v, float))

        self.superior_limit_x_field.value_changed.connect(lambda v: safe_emit_value(self.on_superior_limit_x_changed, v, float))
        self.superior_limit_y_field.value_changed.connect(lambda v: safe_emit_value(self.on_superior_limit_y_changed, v, float))
        self.superior_limit_z_field.value_changed.connect(lambda v: safe_emit_value(self.on_superior_limit_z_changed, v, float))
        self.origin_x_field.value_changed.connect(lambda v: safe_emit_value(self.on_origin_x_changed, v, float))
        self.origin_y_field.value_changed.connect(lambda v: safe_emit_value(self.on_origin_y_changed, v, float))
        self.origin_z_field.value_changed.connect(lambda v: safe_emit_value(self.on_origin_z_changed, v, float))

        self.zero_x_field.value_changed.connect(lambda v: safe_emit_value(self.on_zero_x_changed, v, float))
        self.zero_y_field.value_changed.connect(lambda v: safe_emit_value(self.on_zero_y_changed, v, float))
        self.zero_z_field.value_changed.connect(lambda v: safe_emit_value(self.on_zero_z_changed, v, float))
        
        self.load_button.clicked.connect(self.on_load_dxf_clicked)
        self.process_button.clicked.connect(self.on_process_clicked)
        self.save_button.clicked.connect(self.on_save_rapid_clicked)

class ConfigurationPanel(QWidget):

    load_file_request = Signal()
    process_file_request = Signal()
    save_file_request = Signal()

    def __init__(self, parameters: ProcessingParameters):
        super().__init__()

        self.parameters = parameters
        
        self.current_layout = QHBoxLayout(self)
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()

        self.setup_ui()

        self.connect_signals()

    def setup_ui(self):

        self.left_panel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )

        self.right_panel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )

        self.left_panel.setMinimumWidth(280)
        self.right_panel.setMinimumWidth(320)

        self.current_layout.addWidget(make_scrollable(self.left_panel, scroll_horizontally=False, scroll_vertically=True))
        self.current_layout.addWidget(make_scrollable(self.right_panel, scroll_horizontally=False, scroll_vertically=True))

    def connect_signals(self):
        self.right_panel.on_load_dxf_clicked.connect(self.load_file_request)
        self.right_panel.on_process_clicked.connect(self.process_file_request)
        self.right_panel.on_save_rapid_clicked.connect(self.save_file_request)
        
        # parameters connection
        self.left_panel.on_scale_factor_changed.connect(
            lambda val: self.parameters.set("scale_factor", val)
        )
        self.left_panel.on_float_precision_changed.connect(
            lambda val: self.parameters.set("float_precision", val)
        )
        self.left_panel.on_polyline_velocity_changed.connect(
            lambda val: self.parameters.set("lines_velocity", val)
        )
        self.left_panel.on_arc_velocity_changed.connect(
            lambda val: self.parameters.set("arcs_velocity", val)
        )
        self.left_panel.on_circle_velocity_changed.connect(
            lambda val: self.parameters.set("circles_velocity", val)
        )
        self.left_panel.on_lifting_height_changed.connect(
            lambda val: self.parameters.set("lifting", val)
        )
        self.left_panel.on_auto_trace_changed.connect(
            lambda val: self.parameters.set("use_detector", val)
        )
        self.left_panel.on_offset_programming_changed.connect(
            lambda val: self.parameters.set("use_offset", val)
        )

        self.right_panel.on_inferior_limit_x_changed.connect(
            lambda v: self.parameters.set_workspace_limit(0, 0, v)
        )
        self.right_panel.on_inferior_limit_y_changed.connect(
            lambda v: self.parameters.set_workspace_limit(0, 1, v)
        )
        self.right_panel.on_inferior_limit_z_changed.connect(
            lambda v: self.parameters.set_workspace_limit(0, 2, v)
        )

        self.right_panel.on_superior_limit_x_changed.connect(
            lambda v: self.parameters.set_workspace_limit(1, 0, v)
        )
        self.right_panel.on_superior_limit_y_changed.connect(
            lambda v: self.parameters.set_workspace_limit(1, 1, v)
        )
        self.right_panel.on_superior_limit_z_changed.connect(
            lambda v: self.parameters.set_workspace_limit(1, 2, v)
        )
    