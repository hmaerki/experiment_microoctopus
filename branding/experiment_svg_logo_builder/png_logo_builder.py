# python -m pip install drawsvg[raster]
import pathlib

from PIL import Image, ImageDraw

DIRECTORY_OF_THIS_FILE = pathlib.Path(__file__).parent


def example3():
    stroke_width_mm = 10
    left_left_x = 0
    left_right_x = 200
    right_left_x = left_right_x
    right_right_x = 350
    left_top_y = 0
    left_bottom_y = 120

    radius_mm = 20
    fill = 128

    # Create a new drawing
    im = Image.new(
        "RGBA",
        size=(
            right_right_x - left_left_x + stroke_width_mm,
            left_bottom_y - left_top_y + stroke_width_mm,
        ),
        color="orange",
    )

    def bounding_box(a, b, top: bool, left: bool):
        x0 = min(a[0], b[0])
        x1 = max(a[0], b[0])
        y0 = min(a[1], b[1])
        y1 = max(a[1], b[1])
        if top:
            y1 += y1 - y0
        else:
            y0 -= y1 - y0
        if left:
            x1 += x1 - x0
        else:
            x0 -= x1 - x0
        return (
            x0 - stroke_width_mm // 2,
            y0 - stroke_width_mm // 2,
        ), (
            x1 + stroke_width_mm // 2,
            y1 + stroke_width_mm // 2,
        )

    if True:
        draw = ImageDraw.Draw(im)

        # left: top
        a = left_right_x, left_top_y
        b = left_left_x + radius_mm, left_top_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

        a = b
        b = left_left_x, left_top_y + radius_mm

        draw.arc(
            bounding_box(a, b, top=True, left=True),
            180,
            270,
            fill=fill,
            width=stroke_width_mm,
        )

        # left: left
        a = b
        b = left_left_x, left_bottom_y - radius_mm
        draw.line((a + b), fill=fill, width=stroke_width_mm)

        a = b
        b = left_left_x + radius_mm, left_bottom_y
        draw.arc(
            bounding_box(a, b, top=False, left=True),
            90,
            180,
            fill=fill,
            width=stroke_width_mm,
        )

        # left: bottom
        a = b
        b = left_right_x, left_bottom_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

        # left: left/bottom
        a = b
        b = left_right_x, left_bottom_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

    if True:
        fill = "green"
        draw = ImageDraw.Draw(im)

        # rigth: top
        a = right_left_x, left_top_y
        b = right_right_x - radius_mm, left_top_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

        a = b
        b = right_right_x, left_top_y + radius_mm
        draw.arc(
            bounding_box(a, b, top=True, left=False),
            270,
            0,
            fill=fill,
            width=stroke_width_mm,
        )

        # right: right
        a = b
        b = right_right_x, left_bottom_y - radius_mm
        draw.line((a + b), fill=fill, width=stroke_width_mm)

        a = b
        b = right_right_x - radius_mm, left_bottom_y
        draw.arc(
            bounding_box(a, b, top=False, left=False),
            0,
            90,
            fill=fill,
            width=stroke_width_mm,
        )

        # right: bottom
        a = b
        b = right_left_x, left_bottom_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

        # right: middle
        a = b
        b = right_left_x, left_top_y
        draw.line((a, b), fill=fill, width=stroke_width_mm)

    if False:
        d.append(draw.Text("Simplest Text", font_size=50, x=20, y=60, fill="red"))

    # Display the drawing in Jupyter Notebook or save as an SVG file
    im.save(DIRECTORY_OF_THIS_FILE / "example3.png")
    # d  # Uncomment this line if using Jupyter Notebook to display the drawing inline


if __name__ == "__main__":
    example3()
