# python -m pip install drawsvg[raster]
import pathlib

import drawsvg as draw

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


def example3():
    stroke_width_mm = 20.0
    left_left_x = 0.0
    left_right_x = 200.0
    right_left_x = left_right_x
    right_right_x = 350.0
    left_top_y = 0.0
    left_bottom_y = 120.0

    radius_mm = 20.0

    # Create a new drawing
    d = draw.Drawing(
        right_right_x - left_left_x + stroke_width_mm,
        left_bottom_y - left_top_y + stroke_width_mm,
        origin=(-stroke_width_mm / 2.0, -stroke_width_mm / 2.0),
        displayInline=False,
    )

    if True:
        if False:
            mask = draw.Mask()
            box = draw.Rectangle(30, 50, 100, 100, fill="black")
            mask.append(box)
        else:
            mask = draw.Mask()
            text = draw.Text("Simplest Text", font_size=50, x=0, y=120, fill="black")
            mask.append(text)

        path = draw.Path(
            stroke="yellow",
            stroke_width=stroke_width_mm,
            fill="lightgray",
            # mask=mask,
        )

        # left: right/top
        path.M(left_right_x, left_top_y)

        # left: left/top
        path.L(left_left_x + radius_mm, left_top_y)

        # Rounded left-left/top corner
        path.A(
            radius_mm,
            radius_mm,
            0,
            0,
            0,
            left_left_x,
            left_top_y + radius_mm,
        )

        # left: left/bottom
        path.L(left_left_x, left_bottom_y - radius_mm)

        # Rounded left-left/bottom corner
        path.A(
            radius_mm,
            radius_mm,
            0,
            0,
            0,
            left_left_x + radius_mm,
            left_bottom_y,
        )

        # left: left/bottom
        path.L(left_right_x, left_bottom_y)

        d.append(path)

    if True:
        path = draw.Path(stroke="green", stroke_width=stroke_width_mm, fill="gray")

        # right: left/top
        path.M(right_left_x, left_top_y)

        # right: left/bottom
        path.L(right_left_x, left_bottom_y)

        # right: right/bottom
        path.L(right_right_x - radius_mm, left_bottom_y)

        # Rounded right-right/bottom corner
        # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#elliptical_arc_curve
        path.A(
            radius_mm,
            radius_mm,
            0,
            0,
            0,
            right_right_x,
            left_bottom_y - radius_mm,
        )
        # right: right/top
        path.L(
            right_right_x,
            left_top_y + radius_mm,
        )

        # Rounded right-right/top corner
        path.A(
            radius_mm,
            radius_mm,
            0,
            0,
            0,
            right_right_x - radius_mm,
            left_top_y,
        )

        # Close the path (automatically creates a line back to the start point)
        path.Z()

        d.append(path)

    d.append(draw.Text("Simplest Text", font_size=50, x=20, y=60, fill="red"))

    # Display the drawing in Jupyter Notebook or save as an SVG file
    d.save_png(str(DIRECTORY_OF_THIS_FILE / "rectangle.png"))
    # d  # Uncomment this line if using Jupyter Notebook to display the drawing inline


if __name__ == "__main__":
    example3()
