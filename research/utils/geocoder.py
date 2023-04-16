from .utils import init_logger
from geopandas.tools import geocode
from shapely.geometry.point import Point


class Geocoder:
    """Geocoder class to geocode addresses using geopandas.
    """

    def __init__(self, provider: str, *args, **kwargs):
        self._logger = init_logger()
        self.cache = {}
        self.provider = provider
        self.api_key = kwargs.get("api_key") or self._authenticate()

    def _authenticate(self):
        if self.provider == "GoogleV3":
            import os
            return os.environ["GOOGLE_GEOCODING_API_KEY"]

    def _fetch_cache(self, name: str):
        return self.cache.get(name)

    def _cache_point(self, name: str, point: Point):
        self.cache[name] = point

    def geocode_address(self, name: str, cached: bool = True) -> Point:
        try:
            if cached is True:
                cached_result = self._fetch_cache(name)
                if cached_result is not None:
                    return cached_result

            if self.provider == "GoogleV3":
                self._logger.info(
                    f"Geocoding '{name}' using GoogleV3 API"
                )
                point = geocode(
                    name,
                    provider=self.provider,
                    api_key=self.api_key
                ).geometry[0]
            else:
                point = geocode(
                    name,
                    provider=self.provider,
                ).geometry[0]
            self._cache_point(name=name, point=point)
            return point
        except Exception as e:
            self._logger.error(
                f"Some error occurred trying to geocode '{name}': {e}"
            )
