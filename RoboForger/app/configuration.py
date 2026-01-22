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
)
from PySide6.QtCore import (
    Signal,
    SignalInstance,
)

from RoboForger.app.components.field import Field, LabelPosition
from RoboForger.app.components.separator import LineSeparator
from RoboForger.app.components.label import Label, LabelTag

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
        self.auto_trace: Field
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

        self.scale_factor_field = Field("Scale Factor", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.scale_factor_field)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # converter section
        converter_label = Label("Converter", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(converter_label)

        self.float_precision_field = Field("Float Precision", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.float_precision_field)

        self.polyline_vel_field = Field("Polyline Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.polyline_vel_field)

        self.arc_vel_field = Field("Arc Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.arc_vel_field)

        self.circle_velocity_field = Field("Circle Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.circle_velocity_field)

        self.lifting_height_field = Field("Lifting Height", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.lifting_height_field)

        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # Drawing section
        drawing_label = Label("Drawing and Rapid", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(drawing_label)

        self.auto_trace = Field("Use auto trace detection", QCheckBox(), LabelPosition.RIGHT)
        layout.addWidget(self.auto_trace)

        self.offset_programming_field = Field("Use Offset Programming", QCheckBox(), LabelPosition.RIGHT)
        layout.addWidget(self.offset_programming_field)

        self.setLayout(layout)

    def connect_signals(self):
        self.scale_factor_field.value_changed.connect(lambda v: safe_emit_value(self.on_scale_factor_changed, v, float))
        self.float_precision_field.value_changed.connect(lambda v: safe_emit_value(self.on_float_precision_changed, v, int))
        self.polyline_vel_field.value_changed.connect(lambda v: safe_emit_value(self.on_polyline_velocity_changed, v, float))
        self.arc_vel_field.value_changed.connect(lambda v: safe_emit_value(self.on_arc_velocity_changed, v, float))
        self.circle_velocity_field.value_changed.connect(lambda v: safe_emit_value(self.on_circle_velocity_changed, v, float))
        self.lifting_height_field.value_changed.connect(lambda v: safe_emit_value(self.on_lifting_height_changed, v, float))
        self.auto_trace.value_changed.connect(lambda v: safe_emit_value(self.on_auto_trace_changed, v, bool))
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
        title_label = Label("Coords Parameters", self, tag=LabelTag.HEADER)
        layout.addWidget(title_label)

        # tool section
        tool_label = Label("Tool", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(tool_label)

        self.tool_field = Field("Tool name", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(self.tool_field)

        # workspace limits
        # TODO: implement a small square showing the limit vectors visually
        workspace_label = Label("Workspace Limits InfLeft - SupRight", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(workspace_label)

        vectors_layout = QHBoxLayout()
        
        inf_left_layout = QVBoxLayout()

        self.inferior_limit_x_field = Field("X", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_x_field)

        self.inferior_limit_y_field = Field("Y", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_y_field)

        self.inferior_limit_z_field = Field("Z", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(self.inferior_limit_z_field)

        sup_right_layout = QVBoxLayout()

        self.superior_limit_x_field = Field("X", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_x_field)

        self.superior_limit_y_field = Field("Y", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_y_field)

        self.superior_limit_z_field = Field("Z", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(self.superior_limit_z_field)

        vectors_layout.addLayout(inf_left_layout)
        vectors_layout.addLayout(sup_right_layout)

        layout.addLayout(vectors_layout)

        # References section
        references_label = Label("References", self, tag=LabelTag.SUBHEADER)
        layout.addWidget(references_label)

        references_layout = QHBoxLayout()

        origin_layout = QVBoxLayout()

        self.origin_x_field = Field("Origin X", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_x_field)

        self.origin_y_field = Field("Origin Y", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_y_field)

        self.origin_z_field = Field("Origin Z", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(self.origin_z_field)

        zero_layout = QVBoxLayout()

        self.zero_x_field = Field("Zero X", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_x_field)

        self.zero_y_field = Field("Zero Y", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_y_field)

        self.zero_z_field = Field("Zero Z", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(self.zero_z_field)

        references_layout.addLayout(origin_layout)
        references_layout.addLayout(zero_layout)
        layout.addLayout(references_layout)

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

    def __init__(self):
        super().__init__()
        
        self.current_layout = QHBoxLayout(self)
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()

        self.setup_ui()

    def setup_ui(self):

        self.current_layout.addWidget(self.left_panel)
        self.current_layout.addWidget(self.right_panel)

    def connect_signals(self):
        pass