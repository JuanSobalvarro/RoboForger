from RoboForger import Forger


FILE_NAME = "./test_files/huevo"
PRE_SCALE = 0.3
ORIGIN = (450.0, 0, 375.0)
LIFTING = 50.0
POLYLINE_VELOCITY = 1000
ARC_VELOCITY = 100
CIRCLE_VELOCITY = 100
SPLINE_VELOCITY = 100


def test_rapid():
    # parsing
    forger = Forger(origin=ORIGIN, lifting=LIFTING, pre_scale=PRE_SCALE, float_precision=2, polyline_velocity=POLYLINE_VELOCITY, arc_velocity=ARC_VELOCITY, circle_velocity=CIRCLE_VELOCITY, spline_velocity=SPLINE_VELOCITY,
                    use_intelligent_traces=True, use_offset_programming=True)

    forger.parse_figures(f"{FILE_NAME}.dxf")

    print(f"Raw lines: {forger.get_raw_lines()[0]}...")
    print(f"Raw arcs: {forger.get_raw_arcs()[0]}...")

    forger.convert_figures()

    figures_converted = forger.get_figures()

    print(f"Polylines: {figures_converted.get('polylines', [])[0]}...")
    print(f"Arcs: {figures_converted.get('arcs', [])[0]}...")

    forger.generate_rapid_code()
    
    print("Detected Polylines:", len(figures_converted.get("polylines", [])))
    print("Detected Arcs:", len(figures_converted.get("arcs", [])))
    print("Detected Circles:", len(figures_converted.get("circles", [])))
    print("Detected Splines:", len(figures_converted.get("splines", [])))

    forger.export_rapid_to_txt(f"{FILE_NAME}.txt")


def main():
    test_rapid()

if __name__ == '__main__':
    main()
