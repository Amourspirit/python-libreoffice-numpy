from __future__ import annotations

from .settings import Settings
from ..meta.singleton import Singleton
from ..lo_util.configuration import Configuration


class Options(metaclass=Singleton):
    """Singleton Class. Manages Load Settings for the extension."""

    def __init__(self) -> None:
        settings = Settings()
        self._configuration = Configuration()
        self._node_value = f"/{settings.lo_implementation_name}.Settings/Options"

        self._numpy_requirement = str(settings.current_settings.get("NumpyRequirement", "___numpy_req___"))
        self._load_numpy = bool(settings.current_settings.get("OptionLoadNumpy", False))
        self._load_ooo_dev = bool(settings.current_settings.get("OptionLoadOooDev", False))

    # region Properties
    @property
    def load_numpy(self) -> bool:
        """
        Gets if Numpy should be imported when LibreOffice starts.
        """
        return self._load_numpy

    @property
    def load_ooo_dev(self) -> bool:
        """
        Gets if OOO Dev Tools should be imported when LibreOffice starts.
        """
        return self._load_ooo_dev

    @property
    def numpy_requirement(self) -> str:
        """
        Gets the Numpy Requirement.
        """
        return self._numpy_requirement

    # endregion Properties
