import ezdxf
import os
import subprocess
import io
import tempfile
from typing import List, Tuple, Dict, Any
from RoboForger.fig_types import Point3D, RawLine, RawArc, RawCircle, RawSpline


class DXFParser:
    def __init__(self, stream: io.StringIO):
        try:
            self.doc = ezdxf.read(stream)
        except Exception as e:
            raise ValueError(f"Failed to parse DXF content using ezdxf: {e}")
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
    
def dwg_to_dxf(dwg_filepath: str, tool_path: str) -> str:
    """
    Converts DWG to DXF using LibreDWG's dwg2dxf tool.
    Uses a temporary directory to store the generated DXF.
    Returns DXF content as string.
    """

    if not os.path.exists(tool_path):
        raise FileNotFoundError(f"DWG to DXF converter not found at {tool_path}")

    if not os.path.exists(dwg_filepath):
        raise FileNotFoundError(f"DWG file not found: {dwg_filepath}")

    try:
        # remember to keep the temp directory default to write on Temp, so we don't have to worry about cleaning up files after conversion, and we can be sure that the directory is writable and has enough space for the generated DXF file. 
        # The temporary directory will be automatically deleted after the block is exited, even if an error occurs.
        with tempfile.TemporaryDirectory() as tmpdir:

            base_name = os.path.splitext(os.path.basename(dwg_filepath))[0]
            output_path = os.path.join(tmpdir, base_name + ".dxf")

            # LibreDWG dwg2dxf syntax:
            # dwg2dxf input.dwg -o output.dxf
            cmd = [
                tool_path,
                dwg_filepath,
                "-o",
                output_path,
                "--as=r2018"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            print(f"DWG to DXF conversion stdout:\n{result.stdout}")

            if result.returncode != 0:
                raise RuntimeError(
                    f"DWG to DXF conversion failed:\n{result.stderr}"
                )

            if not os.path.exists(output_path):
                raise RuntimeError("Conversion completed but DXF file not created.")

            # Read DXF content
            with open(output_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    except Exception as e:
        raise RuntimeError(f"Error during DWG to DXF conversion: {e}")

class CADParser:
    def __init__(self, filepath: str, binary_dwg2dxf_path: str, temp_dir: str = "temp"):
        self.filepath = filepath
        self.parser = None
        self.binary_path = binary_dwg2dxf_path
        self.temp_dir = temp_dir

        if not os.path.exists(self.binary_path):
            raise FileNotFoundError(f"CADPARSER::DWG to DXF converter not found at {self.binary_path}")

        file_ext = os.path.splitext(filepath)[1].lower()
        if file_ext == '.dxf':
            stream = io.StringIO()
            with open(filepath, 'r') as f:
                stream.write(f.read())
            stream.seek(0)
            self.parser = DXFParser(stream)
        elif file_ext == '.dwg':
            dxf_content = dwg_to_dxf(filepath, self.binary_path)
            # dxf_content = clean_dxf_content(dxf_content)
            # print(f"New lines in DXF content: {sdxf_content.count('\n')}. Lines: {len(dxf_content.splitlines())}")
            if dxf_content:
                stream = io.StringIO(initial_value=dxf_content)
                stream.seek(0)

                # debug save file
                # output_path = os.path.splitext(filepath)[0] + ".dxf"
                # with open(output_path, 'w') as f:
                #     f.write(stream.getvalue())

                self.parser = DXFParser(stream)

            else:
                raise ValueError(f"CADPARSER::Failed to convert DWG to DXF: {filepath}")
        else:
            raise ValueError(f"CADPARSER::Unsupported file format: {file_ext}")

    def get_figures_parsed(self) -> Dict[str, Any]:
        if self.parser:
            return self.parser.get_figures_parsed()
        else:
            raise ValueError("No parser available for the given file.")