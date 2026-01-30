import ezdxf
import os
import subprocess
from typing import List, Tuple, Dict, Any
from RoboForger.fig_types import Point3D, RawLine, RawArc, RawCircle, RawSpline


BINARY_DWG2DXF_PATH = os.path.join(os.path.dirname(__file__), 'bin', 'libredwg', 'dwg2dxf.exe')

class DXFParser:
    def __init__(self, filepath: str):
        self.doc = ezdxf.readfile(filepath)
        self._msp = self.doc.modelspace()

    def set_doc(self, file_path: str):

        if os.path.exists(file_path):
            self.doc = ezdxf.readfile(file_path)
            self._msp = self.doc.modelspace()

            return f"File: {file_path} loaded correctly"

        return f"File: {file_path} could not be loaded"

    def get_lines(self) -> List[RawLine]:
        lines = []
        for e in self._msp.query('LINE'):
            start = (e.dxf.start.x, e.dxf.start.y, getattr(e.dxf.start, 'z', 0.0))
            end = (e.dxf.end.x, e.dxf.end.y, getattr(e.dxf.end, 'z', 0.0))
            lines.append({'start': start, 'end': end})
        return lines

    def get_circles(self) -> List[RawCircle]:
        circles = []
        for e in self._msp.query('CIRCLE'):
            center = (e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0))
            radius = e.dxf.radius
            circles.append({'center': center, 'radius': radius})
        return circles

    def get_arcs(self) -> List[RawArc]:
        """
        Returns a list of arcs represented by:
        (center, radius, start_point, end_point, start_angle, end_angle, clockwise)
        """
        arcs = []
        for e in self._msp.query('ARC'):
            center = (e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0))
            radius = e.dxf.radius

            start_angle = e.dxf.start_angle
            end_angle = e.dxf.end_angle

            arcs.append({'center': center, 'radius': radius, 'start_angle': start_angle, 'end_angle': end_angle, 'clockwise': False})
        return arcs

    def get_splines(self) -> List[RawSpline]:
        """
        Returns a list of splines represented by
        """
        splines = []
        for e in self._msp.query('SPLINE'):
            # just for testing if it works
            # print(f"Spline: {e} - Degree: {e.dxf.degree} - Closed: {e.closed}. Control points{len(e.control_points)}: {e.control_points}. Weights: {e.weights}. Knots: {e.knots}. Fit points: {e.fit_points}")
            splines.append(
                {
                    'degree': e.dxf.degree,
                    'closed': e.closed,
                    'knots': e.knots,
                    'weights': e.weights,
                    'control_points': [(pt[0], pt[1], 0.0) for pt in e.control_points],
                    'fit_points': [(pt[0], pt[1], 0.0) for pt in e.fit_points],
                }
            )
        return splines

    def get_figures_parsed(self) -> Dict[str, Any]:
        """
        Returns a dictionary with all figures parsed from the DXF file.
        """
        return {
            'lines': self.get_lines(),
            'arcs': self.get_arcs(),
            'circles': self.get_circles(),
            'splines': self.get_splines()
        }
    
def dwg_to_dxf(dwg_filepath: str, output_filepath: str, tool_path: str) -> bool:
    """
    Converts the DWG file to DXF format using the `dwg2dxf` command line tool.
    
    :param dwg_filepath: Path to the input DWG file.
    :param output_filepath: Path to save the converted DXF file.
    :return: True if conversion was successful, False otherwise.
    """
    if not os.path.exists(tool_path):
        raise FileNotFoundError(f"DWG to DXF converter not found at {tool_path}")
    
    try:
        result = subprocess.run([tool_path, dwg_filepath, '-o', output_filepath, '-y'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"DWG to DXF conversion failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error converting DWG to DXF: {e}")
        return False
    
    return result.returncode == 0

class CADParser:
    def __init__(self, filepath: str, binary_dwg2dxf_path: str):
        self.filepath = filepath
        self.parser = None
        self.binary_path = binary_dwg2dxf_path

        if not os.path.exists(self.binary_path):
            raise FileNotFoundError(f"CADPARSER::DWG to DXF converter not found at {self.binary_path}")

        file_ext = os.path.splitext(filepath)[1].lower()
        if file_ext == '.dxf':
            self.parser = DXFParser(filepath)
        elif file_ext == '.dwg':
            # Convert DWG to DXF first
            dxf_temp_path = filepath + '.dxf'
            print(f"Temporal path for DXF: {dxf_temp_path}")
            if dwg_to_dxf(filepath, dxf_temp_path, self.binary_path):
                self.parser = DXFParser(dxf_temp_path)
            else:
                raise ValueError(f"CADPARSER::Failed to convert DWG to DXF: {filepath}")
            
            # clean dxf
            if os.path.exists(dxf_temp_path):
                os.remove(dxf_temp_path)
        else:
            raise ValueError(f"CADPARSER::Unsupported file format: {file_ext}")

    def get_figures_parsed(self) -> Dict[str, Any]:
        if self.parser:
            return self.parser.get_figures_parsed()
        else:
            raise ValueError("No parser available for the given file.")