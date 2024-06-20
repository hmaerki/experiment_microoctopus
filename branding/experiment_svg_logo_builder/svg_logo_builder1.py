# python -m pip install drawsvg[raster]
import pathlib

import drawsvg as draw

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


def example1():
    d = draw.Drawing(200, 100, origin="center")

    # Draw an irregular polygon
    d.append(
        draw.Lines(
            -80,
            45,
            70,
            49,
            95,
            -49,
            -90,
            -40,
            close=False,
            fill="#eeee00",
            stroke="black",
        )
    )

    # Draw a rectangle
    r = draw.Rectangle(-80, -50, 40, 50, fill="#1248ff")
    r.append_title("Our first rectangle")  # Add a tooltip
    d.append(r)

    # Draw a circle
    d.append(draw.Circle(-40, 10, 30, fill="red", stroke_width=2, stroke="black"))

    # Draw an arbitrary path (a triangle in this case)
    p = draw.Path(stroke_width=2, stroke="lime", fill="black", fill_opacity=0.2)
    p.M(-10, -20)  # Start path at point (-10, -20)
    p.C(30, 10, 30, -50, 70, -20)  # Draw a curve to (70, -20)
    d.append(p)

    # Draw text
    d.append(
        draw.Text("Basic text", 8, -10, -35, fill="blue")
    )  # 8pt text at (-10, -35)
    d.append(draw.Text("Path text", 8, path=p, text_anchor="start", line_height=1))
    d.append(
        draw.Text(["Multi-line", "text"], 8, path=p, text_anchor="end", center=True)
    )

    # Draw multiple circular arcs
    d.append(
        draw.ArcLine(
            60,
            20,
            20,
            60,
            270,
            stroke="red",
            stroke_width=5,
            fill="red",
            fill_opacity=0.2,
        )
    )
    d.append(
        draw.Arc(
            60, 20, 20, 90, -60, cw=True, stroke="green", stroke_width=3, fill="none"
        )
    )
    d.append(
        draw.Arc(
            60,
            20,
            20,
            -60,
            90,
            cw=False,
            stroke="blue",
            stroke_width=1,
            fill="black",
            fill_opacity=0.3,
        )
    )

    # Draw arrows
    arrow = draw.Marker(-0.1, -0.51, 0.9, 0.5, scale=4, orient="auto")
    arrow.append(draw.Lines(-0.1, 0.5, -0.1, -0.5, 0.9, 0, fill="red", close=True))
    p = draw.Path(
        stroke="red", stroke_width=2, fill="none", marker_end=arrow
    )  # Add an arrow to the end of a path
    p.M(20, 40).L(20, 27).L(0, 20)  # Chain multiple path commands
    d.append(p)
    d.append(
        draw.Line(
            30, 20, 0, 10, stroke="red", stroke_width=2, fill="none", marker_end=arrow
        )
    )  # Add an arrow to the end of a line

    d.set_pixel_scale(2)  # Set number of pixels per geometry unit
    # d.set_render_size(400, 200)  # Alternative to set_pixel_scale
    d.save_svg(str(DIRECTORY_OF_THIS_FILE / "example.svg"))
    d.save_png(str(DIRECTORY_OF_THIS_FILE / "example.png"))

    # Display in Jupyter notebook
    # d.rasterize()  # Display as PNG
    d  # Display as SVG


def example2():
    stroke_width_mm = 20.0
    rect_width_mm = 450.0
    rect_height_mm = 150.0
    radius_mm = 60.0
    # Create a new drawing
    d = draw.Drawing(
        rect_width_mm + stroke_width_mm,
        rect_height_mm + stroke_width_mm,
        origin="center",
        displayInline=False,
    )

    d.append(
        draw.Rectangle(
            -rect_width_mm / 2.0,
            -rect_height_mm / 2.0,
            rect_width_mm,
            rect_height_mm,
            rx=radius_mm,
            ry=radius_mm,
            fill="none",
            stroke="yellow",
            stroke_width=stroke_width_mm,
        )
    )

    # Filled rectangle on the right half
    d.append(
        draw.Rectangle(
            0,  # Starts from the center, covering the right half
            -rect_height_mm / 2.0,
            rect_width_mm / 2.0,  # Half the width to cover the right side
            rect_height_mm - stroke_width_mm,
            fill="yellow",  # Fill color
        )
    )

    # Display the drawing in Jupyter Notebook or save as an SVG file
    d.save_png(str(DIRECTORY_OF_THIS_FILE / "rectangle.png"))
    # d  # Uncomment this line if using Jupyter Notebook to display the drawing inline


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

    if False:
        d.append(
            draw.Rectangle(
                -rect_width_mm / 2.0,
                -rect_height_mm / 2.0,
                rect_width_mm,
                rect_height_mm,
                rx=radius_mm,
                ry=radius_mm,
                fill="none",
                stroke="yellow",
                stroke_width=stroke_width_mm,
            )
        )

    # Filled rectangle on the right half
    # d.append(
    #     draw.Rectangle(
    #         0,  # Starts from the center, covering the right half
    #         -rect_height_mm / 2.0,
    #         rect_width_mm / 2.0,  # Half the width to cover the right side
    #         rect_height_mm - stroke_width_mm,
    #         fill="yellow",  # Fill color
    #     )
    # )
    if False:
        g = draw.Group()
        rect = draw.Rectangle(10, 10, 100, 200, fill="black")
        text = draw.Text("Simplest Text", font_size=50, x=0, y=120, fill="white")
        g.append(rect)
        g.append(text)
        d.append(g)
        mask = Mask()
        mask.append(g)
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
