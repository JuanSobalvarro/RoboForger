from RoboForger.forger.cad_parser import CADParser
from RoboForger.forger.converter import Converter
from RoboForger.drawing.draw import Draw
from RoboForger.utils import export_str2txt


FILE_NAME = "./test_files/formula"

def test_rapid():
    parser = CADParser(filepath=f'{FILE_NAME}.dxf', scale=1.0)
    lines = parser.get_lines()
    raw_arcs = parser.get_arcs()
    raw_circles = parser.get_circles()

    converter = Converter(float_precision=4)
    polylines = converter.convert_lines_to_polylines(lines)
    arcs = converter.convert_arcs(raw_arcs)
    circles = converter.convert_circles(raw_circles)

    print("Detected Polylines:", len(polylines))
    print("Detected Arcs:", len(arcs))
    print("Detected Circles:", len(circles))

    for circle in circles:
        circle.set_velocity(100)

    for arc in arcs:
        arc.set_velocity(100)

    draw = Draw(use_detector=True)

    draw.add_figures(polylines)
    draw.add_figures(arcs)
    draw.add_figures(circles)

    export_str2txt(draw.generate_rapid_code(use_offset=True), filepath=f"{FILE_NAME}.txt")

def main():
    test_rapid()

if __name__ == '__main__':
    main()
