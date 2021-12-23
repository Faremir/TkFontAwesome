from lxml import etree
from pathlib import Path
import io
import tksvg


def icon_to_image(name, fill=None, scale_to_width=None, scale_to_height=None, scale=1):
    """Lookup an svg file by name and return as an SvgImage object that
    can be used anywhere a PhotoImage object is used in tkinter.

    Parameters:

        name (str):
            The name of the FontAwesome icon. The icon name can be
            found at https://fontawesome.com/v5.0/icons. Only the free
            categories are available in this library.

        fill (str):
            Sets the fill color of the svg path.

        scale_to_width (int):
            Adjust to image size to this width in pixels. Maintains
            the view's aspect ratio.

        scale_to_height (int):
            Adjust to image size to this height in pixels. Maintains
            the view's aspect ratio.

        scale (float):
            Scale the image width and height by this factor.

    Returns:

        SvgImage:
            The converted svg image

    Examples:

        ```python
        import tkinter as tk
        from tkfontawesome import icon_to_image

        root = tk.Tk()
        img = icon_to_image("facebook", fill="#4267B2", scale_to_width=64)

        tk.Label(root, image=img).pack(padx=10, pady=10)

        root.mainloop()
        ```
    """
    file = _get_icon_file(name)
    img_data = svg_to_image(file, fill, scale_to_width, scale_to_height, scale)
    return img_data


def svg_to_image(source, fill=None, scale_to_width=None, scale_to_height=None, scale=1):
    """Opens and svg file and returns an SvgImage object that can be
    used anywhere you would use a tkinter.PhotoImage.

    Parameters:
        source (Union[str, FileObj]):
            Filename or file object containing svg data.

        fill (str):
            Sets the fill color of the svg path.

        scale_to_width (int):
            Adjust to image size to this width in pixels. Maintains
            the view's aspect ratio.

        scale_to_height (int):
            Adjust to image size to this height in pixels. Maintains
            the view's aspect ratio.

        scale (float):
            Scale the image width and height by this factor.

        **kwargs (Dict):
            Other keyword arguments.

    Returns:

        SvgImage:
            The converted svg image
    """
    # parse xml data
    with open(source) as p:
        tree = etree.parse(source=p)
        root = tree.getroot()

    # set path fill color if provided
    if fill is not None:
        root.attrib["fill"] = fill

    imgdata = io.BytesIO()
    tree.write(imgdata)
    kw = {"data": imgdata.getvalue()}
    if scale_to_width:
        kw["scaletowidth"] = scale_to_width
    if scale_to_height:
        kw["scaletoheight"] = scale_to_height
    if scale != 1:
        kw["scale"] = scale

    return tksvg.SvgImage(**kw)


def _collect_svg_files():
    files = []
    root = Path(__file__).parent
    files.extend(root.joinpath("svgs", "brands").iterdir())
    files.extend(root.joinpath("svgs", "regular").iterdir())
    files.extend(root.joinpath("svgs", "solid").iterdir())
    return files


def _get_icon_file(name):
    files = _collect_svg_files()
    for file in files:
        if file.stem == name:
            return file
    raise Exception(
        f"'{name}' is not a valid icon name. Check spelling and consult https://fontawesome.com/v5.0/icons."
    )