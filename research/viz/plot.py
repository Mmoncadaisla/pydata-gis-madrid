import pandas as pd
import numpy as np
import jinja2
from ipywidgets import HTML

MAX_QCUT_ITERS = 10

NULL_COLOR_RGB = [204, 204, 204]

ACCEPTED_BREAKS_METHODS = ['equal-size', 'equal-interval']

# CartoColors palettes, see https://carto.com/carto-colors/
PALETTES_HEX = {
    "sunset": [
        "#f3e79b",
        "#fac484",
        "#f8a07e",
        "#eb7f86",
        "#ce6693",
        "#a059a0",
        "#5c53a5",
    ],
    "burg": [
        "#ffc6c4",
        "#f4a3a8",
        "#e38191",
        "#cc607d",
        "#ad466c",
        "#8b3058",
        "#672044",
    ],
    "oryel": [
        "#ecda9a",
        "#efc47e",
        "#f3ad6a",
        "#f7945d",
        "#f97b57",
        "#f66356",
        "#ee4d5a",
    ],
    "temps": [
        "#009392",
        "#39b185",
        "#9ccb86",
        "#e9e29c",
        "#eeb479",
        "#e88471",
        "#cf597e",
    ],
    "tealrose": [
        "#009392",
        "#72aaa1",
        "#b1c7b3",
        "#f1eac8",
        "#e5b9ad",
        "#d98994",
        "#d0587e",
    ],
    "pastel": [
        "#66C5CC",
        "#F6CF71",
        "#F89C74",
        "#DCB0F2",
        "#87C55F",
        "#9EB9F3",
        "#FE88B1",
        "#C9DB74",
        "#8BE0A4",
        "#B497E7",
        "#D3B484",
        "#B3B3B3",
    ],
    "safe": [
        "#88CCEE",
        "#CC6677",
        "#DDCC77",
        "#117733",
        "#332288",
        "#AA4499",
        "#44AA99",
        "#999933",
        "#882255",
        "#661100",
        "#6699CC",
        "#888888",
    ],
    "prism": [
        "#5F4690",
        "#1D6996",
        "#38A6A5",
        "#0F8554",
        "#73AF48",
        "#EDAD08",
        "#E17C05",
        "#CC503E",
        "#94346E",
        "#6F4070",
        "#994E95",
        "#666666",
    ],
}


def _get_equal_break_legend_values(
    breaks_values: np.ndarray,
    palette_steps: np.ndarray,
    null_color: list = NULL_COLOR_RGB,
) -> list:
    rgb = list(palette_steps)
    breaks = list(breaks_values[:len(rgb)])
    others_category = [
        {"text": "Others", "color": null_color}
        ] if len(rgb) < len(list(breaks_values)) else []
    first_value = [{"text": f"Values <= {breaks[0]}", "color": rgb[0]}]
    other_values = [{"text": f">{lo} and <={hi}", "color": c}
                    for lo, hi, c in zip(breaks[:-1], breaks[1:], rgb[1:])]
    return first_value + other_values + others_category


def _get_category_legend_values(
    categories: np.ndarray,
    palette_steps: np.ndarray,
    null_color: list = NULL_COLOR_RGB
) -> list:
    rgb = list(palette_steps)
    display_categories = list(categories[:len(rgb)])
    others_category = [
        {"text": "Others", "color": null_color}
        ] if len(rgb) < len(categories) else []
    return [{"text": c, "color": rgb[i]}
            for i, c in enumerate(display_categories)] + others_category


def create_legend(
    labels: list,
    title: str,
    footer: str,
    as_html: bool = True
):
    """
    Creates an HTML legend from a list dictionary of the format
        {'text': str, 'color': [r, g, b]}

    Args:
        labels (list): List of dictionaries
                       with the format {'text': str, 'color': [r, g, b]}
        title (str): Legend title
        footer (str): Legend footer

    Returns:
        HTML or str: Legend
    """
    labels = list(labels)
    for label in labels:
        assert list(label['color']) and list(label['text'])
        assert len(label['color']) in (3, 4)
        label['color'] = ', '.join([str(c) for c in label['color']])
    legend_template = jinja2.Template('''
    <style>
      .legend {
        width: 300px;
      }
      .square {
        height: 10px;
        width: 10px;
        border: 1px solid grey;
      }
      .left {
        float: left;
      }
      .right {
        float: right;
      }
    </style>
    <h2>{{ title }}</h2>
    {% for label in labels %}
    <div class='legend'>
      <div class="square left"
        style="background:rgba({{ label['color'] }})"></div>
      <span class="right">{{label['text']}}</span>
      <br />
    </div>
    {% endfor %}
    <br />
    <p>{{ footer }}</p>
    ''')
    html_str = legend_template.render(
        labels=labels, title=title, footer=footer
    )
    if as_html is True:
        return HTML(html_str)
    else:
        return html_str


def hex_to_rgb(hex: str) -> tuple:
    """Function to convert hex color to rgb

    Args:
        hex (str): Hex color code

    Returns:
        tuple: RGB color code
    """
    hex = hex.replace("#", "")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def get_rgb_palette(palette: str) -> np.array:
    """Function to get RGB palette

    Args:
        palette (str): Palette name

    Returns:
        np.array: RGB palette
    """
    norm_palette = palette.lower()
    hex_palette = PALETTES_HEX.get(norm_palette)
    if hex_palette:
        return np.array([hex_to_rgb(hex) for hex in hex_palette])


def get_df_breaks_values(
    df,
    col: str,
    intervals: int,
    how='equal-size'
) -> np.ndarray:
    """Function to get intervals from a DataFrame

    Args:
        df (pd.DataFrame or gpd.GeoDataFrame): DataFrame
        col (str): Column name
        intervals (int): Number of intervals

    Returns:
        np.ndarray: Breaks values
    """
    breaks = intervals - 1
    series = df[col].dropna()
    if how not in (ACCEPTED_BREAKS_METHODS):
        raise ValueError(
            f"Invalid breaks method. Must be one of {ACCEPTED_BREAKS_METHODS}")
    if how == 'equal-size':
        num_iters = 0
        while True:
            breaks_values = pd.qcut(
                series,
                q=breaks,
                retbins=True,
                duplicates="drop"
            )[1]
            num_iters += 1

            if (len(breaks_values) >= breaks) or (num_iters > MAX_QCUT_ITERS):
                break
            else:
                breaks += 1

    elif how == 'equal-interval':
        breaks_values = pd.cut(
            series,
            bins=breaks,
            retbins=True,
            duplicates="drop"
        )[1]
    return breaks_values


def get_palette_steps(palette: str, steps: int) -> np.ndarray:
    """Function to get palette steps

    Args:
        palette (str): Palette name
        steps (int): Number of steps

    Returns:
        np.ndarray: Palette steps
    """
    rgb_palette = get_rgb_palette(palette)
    row_indices = np.linspace(0, rgb_palette.shape[0] - 1, steps, dtype=int)
    return rgb_palette[row_indices]


def equal_color_intervals(
    df,
    col: str,
    palette: str,
    intervals: int,
    how: str = 'equal-size',
    null_color: list = NULL_COLOR_RGB,
    return_legend: bool = False,
    legend_title: str = None,
    legend_footer: str = None,
    legend_as_html: bool = True,
) -> str:
    """Function to generate a deck.gl expression to color bins

    Args:
        df (DataFrame): Pandas or GeoPandas DataFrame
        col (str): Column name
        palette (str): Palette name
        breaks (int): Number of breaks
        how (str, optional): How to calculate the breaks.
                             Methods are 'equal-size' and 'equal-interval'.
        null_color (list, optional): RGB color list for null values.
                                     Defaults to NULL_COLOR_RGB.

    Raises:
        ValueError: If the number of breaks is lower than 1.
        ValueError: If the number of breaks is higher than the number
                    of palette steps

    Returns:
        str: Deck.gl expression
    """
    legend = None

    full_palette_values = get_rgb_palette(palette)
    n_palette_values = len(full_palette_values)

    if intervals <= 0:
        raise ValueError("The number of intervals needs to be higher than 0")

    if intervals > n_palette_values:
        raise ValueError(
            f"Cannot allocate palette '{palette}'"
            f"for the number of breaks '{intervals}' "
            f"(maximum is: {n_palette_values}), "
            "please reduce the breaks value or choose a different palette"
        )

    breaks_values = get_df_breaks_values(
        df=df,
        col=col,
        intervals=intervals,
        how=how
    )

    palette_steps = get_palette_steps(
        palette=palette, steps=len(breaks_values)
    )

    value_color_list = zip(breaks_values, palette_steps)

    exp_list = [f"{col} <= {val} ? {color}" for val, color in value_color_list]

    deckgl_expression = f"{' : '.join(exp_list)} : {null_color}"

    if return_legend is True:
        title = legend_title if legend_title else col
        labels_dict_list = _get_equal_break_legend_values(
            breaks_values,
            palette_steps
        )
        legend = create_legend(
            labels=labels_dict_list,
            title=title,
            footer=legend_footer,
            as_html=legend_as_html,
        )

    return (deckgl_expression, legend)


def category_color_intervals(
    df,
    col: str,
    palette: str,
    null_color: list = NULL_COLOR_RGB,
    return_legend: bool = False,
    legend_title: str = None,
    legend_footer: str = None,
    legend_as_html: bool = True,
) -> str:
    """Function to generate a deck.gl expression to color categories

    Args:
        df (pd.DataFrame or gpd.GeoDataFrame): DataFrame
        col (str): Column name
        palette (str): Palette name
        null_color (list, optional): Null color RGB value.
                                    Defaults to NULL_COLOR_RGB.

    Returns:
        str: Deck.gl expression
    """
    legend = None

    full_palette_values = get_rgb_palette(palette)

    categories = df[col].unique()

    palette_steps = full_palette_values[:len(categories)]

    value_color_list = zip(categories, palette_steps)

    exp_list = [f"{col} === '{val}' ? {color}" for
                val, color in value_color_list]

    deckgl_expression = f"{' : '.join(exp_list)} : {null_color}"

    if return_legend is True:
        title = legend_title if legend_title else col
        labels_dict_list = _get_category_legend_values(
            categories,
            palette_steps,
            null_color=null_color
        )
        legend = create_legend(
            labels=labels_dict_list,
            title=title,
            footer=legend_footer,
            as_html=legend_as_html,
        )

    return (deckgl_expression, legend)
