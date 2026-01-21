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
from RoboForger.app.components.field import Field, LabelPosition
from RoboForger.app.components.separator import LineSeparator


class LeftPanel(QFrame):
    def __init__(self):
        super().__init__()

        layout: QLayout = QVBoxLayout(self)

        # Title label
        title_label = QLabel("Robo Parameters", self)
        layout.addWidget(title_label)

        # parser section
        parser_label = QLabel("Parser", self)
        layout.addWidget(parser_label)

        scale_factor_field = Field("Scale Factor", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(scale_factor_field)

        # separator
        separator = LineSeparator('horizontal')
        layout.addWidget(separator)

        # converter section
        converter_label = QLabel("Converter", self)
        layout.addWidget(converter_label)

        float_precision_field = Field("Float Precision", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(float_precision_field)

        polyline_vel_field = Field("Polyline Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(polyline_vel_field)

        arc_vel_field = Field("Arc Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(arc_vel_field)

        circle_velocity_field = Field("Circle Velocity", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(circle_velocity_field)

        lifting_height_field = Field("Lifting Height", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(lifting_height_field)

        # Drawing section
        drawing_label = QLabel("Drawing and Rapid", self)
        layout.addWidget(drawing_label)

        auto_trace = Field("Use auto trace detection", QCheckBox(), LabelPosition.RIGHT)
        layout.addWidget(auto_trace)

        offset_programming_field = Field("Use Offset Programming", QCheckBox(), LabelPosition.RIGHT)
        layout.addWidget(offset_programming_field)

        self.setLayout(layout)


class RightPanel(QFrame):
    def __init__(self):
        super().__init__()

        layout: QLayout = QVBoxLayout(self)

        # Title label
        title_label = QLabel("Coords Parameters", self)
        layout.addWidget(title_label)

        # tool section
        tool_label = QLabel("Tool", self)
        layout.addWidget(tool_label)

        tool_field = Field("Tool name", QLineEdit(), LabelPosition.LEFT)
        layout.addWidget(tool_field)

        # workspace limits
        # TODO: implement a small square showing the limit vectors visually
        workspace_label = QLabel("Workspace Limits InfLeft - SupRight", self)
        layout.addWidget(workspace_label)

        vectors_layout = QHBoxLayout()
        
        inf_left_layout = QVBoxLayout()

        inf_left_x_field = Field("X", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(inf_left_x_field)

        inf_left_y_field = Field("Y", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(inf_left_y_field)

        inf_left_z_field = Field("Z", QLineEdit(), LabelPosition.LEFT)
        inf_left_layout.addWidget(inf_left_z_field)

        sup_right_layout = QVBoxLayout()

        sup_right_x_field = Field("X", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(sup_right_x_field)

        sup_right_y_field = Field("Y", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(sup_right_y_field)

        sup_right_z_field = Field("Z", QLineEdit(), LabelPosition.RIGHT)
        sup_right_layout.addWidget(sup_right_z_field)

        vectors_layout.addLayout(inf_left_layout)
        vectors_layout.addLayout(sup_right_layout)

        layout.addLayout(vectors_layout)

        # References section
        references_label = QLabel("References", self)
        layout.addWidget(references_label)

        references_layout = QHBoxLayout()

        origin_layout = QVBoxLayout()

        origin_x_field = Field("Origin X", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(origin_x_field)

        origin_y_field = Field("Origin Y", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(origin_y_field)

        origin_z_field = Field("Origin Z", QLineEdit(), LabelPosition.LEFT)
        origin_layout.addWidget(origin_z_field)

        zero_layout = QVBoxLayout()

        zero_x_field = Field("Zero X", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(zero_x_field)

        zero_y_field = Field("Zero Y", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(zero_y_field)

        zero_z_field = Field("Zero Z", QLineEdit(), LabelPosition.RIGHT)
        zero_layout.addWidget(zero_z_field)

        references_layout.addLayout(origin_layout)
        references_layout.addLayout(zero_layout)
        layout.addLayout(references_layout)

        # Processing section
        # temporal buttons since we should use custom ones with icons later
        load_button = QPushButton("Load DXF", self)
        process_button = QPushButton("Process", self)
        save_button = QPushButton("Save RAPID", self)
        layout.addWidget(load_button)
        layout.addWidget(process_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

class ConfigurationPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.current_layout = QHBoxLayout(self)
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()

        self.setup_ui()

    def setup_ui(self):

        self.current_layout.addWidget(self.left_panel)
        self.current_layout.addWidget(self.right_panel)
