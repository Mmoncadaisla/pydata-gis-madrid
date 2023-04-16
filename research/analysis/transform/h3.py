import h3
import numpy as np
import pandas as pd
import rasterio
import shapely

from h3ronpy.raster import nearest_h3_resolution, raster_to_dataframe

DEFAULT_H3RONPY_H3_COL_NAME = "h3index"


def point_to_h3(point: shapely.Point, resolution: int) -> str:
    """Function to convert a point to an H3 index.

    Args:
        point (shapely.Point): Point to convert to H3 index.
        resolution (int): H3 resolution.

    Returns:
        str: H3 index in string format.
    """
    return h3.latlng_to_cell(point.y, point.x, resolution)


def raster_band_to_pandas_h3(
    band: np.array,
    raster: rasterio.io.DatasetReader,
    res: int = None,
    search_mode: str = "nearest",
    h3_as_str: bool = True,
    h3_col_name: str = "h3",
    add_geom: bool = False,
) -> pd.DataFrame:
    """Function to convert a raster band to a pandas dataframe with H3 indices.

    Args:
        band (np.array): Raster band to convert to H3 dataframe.
        raster (rasterio.io.DatasetReader): Rasterio raster object.
        res (int, optional): H3 Resolution. Defaults to None.
                             If not provided, will be inferred from raster.
        search_mode (str, optional): Search mode to infer H3 resolution.
                                     Defaults to "nearest".
        h3_as_str (bool, optional): Return H3 indexes in string format.
                                    Defaults to True.
        h3_col_name (str, optional): Name of the H3 column. Defaults to "h3".
        add_geom (bool, optional): Add H3 boundary geometry. Defaults to False.

    Returns:
        pd.DataFrame: Pandas dataframe with H3 indexes and band information.
    """
    if not res:
        print(
            "Looking for raster band H3 resolution "
            f"using search_mode {search_mode}..."
        )
        res = nearest_h3_resolution(
            band.shape, raster.transform, search_mode=search_mode
        )

    h3_df = raster_to_dataframe(
        band, raster.transform, res, compacted=False, geo=add_geom
    ).rename(columns={DEFAULT_H3RONPY_H3_COL_NAME: h3_col_name})
    if h3_as_str is True:
        h3_df[h3_col_name] = h3_df[h3_col_name].apply(h3.int_to_str)
    return h3_df
