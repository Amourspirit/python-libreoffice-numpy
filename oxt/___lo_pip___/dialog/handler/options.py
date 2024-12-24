from __future__ import annotations
from typing import Any, TYPE_CHECKING, List, cast
import contextlib

import uno
import unohelper

from com.sun.star.awt import XContainerWindowEventHandler
from com.sun.star.beans import PropertyChangeEvent  # struct
from com.sun.star.beans import XPropertyChangeListener

from ...basic_config import BasicConfig
from ...lo_util.resource_resolver import ResourceResolver

from ...lo_util.configuration import Configuration, SettingsT
from ...settings.settings import Settings
from ...oxt_logger import OxtLogger

# from ...ver.req_version import ReqVersion
from ...ver.rules.ver_rules import VerRules
from ..message_dialog import MessageDialog
from packaging.version import InvalidVersion

if TYPE_CHECKING:
    from com.sun.star.awt import UnoControlDialog  # service
    from com.sun.star.awt import UnoControlEdit  # service
    from com.sun.star.awt import UnoControlCheckBoxModel


IMPLEMENTATION_NAME = f"{BasicConfig().lo_implementation_name}.OptPage"


class CheckBoxListener(unohelper.Base, XPropertyChangeListener):
    def __init__(self, handler: "OptionsDialogHandler"):
        self._logger = OxtLogger(log_name=__name__)
        self._logger.debug("CheckBoxListener.__init__")
        self.handler = handler
        self._logger.debug("CheckBoxListener.__init__ done")

    def disposing(self, Source: Any):
        pass

    def propertyChange(self, evt: PropertyChangeEvent):
        self._logger.debug("CheckBoxListener.propertyChange")
        try:
            # state (evn.NewValue) will be 1 for true and 0 for false
            src = cast("UnoControlCheckBoxModel", evt.Source)
            if src.Name == "chkNumpy":
                self.handler.load_numpy = self.handler.state_to_bool(
                    cast(int, (evt.NewValue))
                )
        except Exception as err:
            self._logger.error(f"CheckBoxListener.propertyChange: {err}", exc_info=True)
            raise


class OptionsDialogHandler(unohelper.Base, XContainerWindowEventHandler):
    def __init__(self, ctx: Any):
        self._logger = OxtLogger(log_name=self.__class__.__name__)
        self._logger.debug("OptionPage-OptionsDialogHandler.__init__")
        self.ctx = ctx
        self._config = BasicConfig()
        self._resource_resolver = ResourceResolver(self.ctx)
        self._config_node = f"/{self._config.lo_implementation_name}.Settings/Options"
        self._window_name = "options"
        self._settings = Settings()
        self._load_numpy = False
        self._load_numpy_original = False
        self._numpy_requirement = ""
        self._numpy_requirement_original = ""
        self._logger.debug("OptionPage-OptionsDialogHandler.__init__ done")

    # region XContainerWindowEventHandler
    def callHandlerMethod(  # type: ignore
        self, xWindow: UnoControlDialog, EventObject: Any, MethodName: str
    ) -> bool:  # type: ignore
        self._logger.debug("callHandlerMethod: %s", MethodName)
        if MethodName == "external_event":
            try:
                return self._handle_external_event(xWindow, EventObject)
            except Exception as e:
                print(e)
        return True

    def getSupportedMethodNames(self):
        return ("external_event",)

    # endregion XContainerWindowEventHandler

    def _has_log_options_changed(self):
        if self._numpy_requirement != self._numpy_requirement_original:
            return True
        return self.load_numpy != self._load_numpy_original

    def _handle_external_event(self, window: UnoControlDialog, ev_name: str):
        self._logger.debug("_handle_external_event: %s", ev_name)
        if ev_name == "ok":
            self._save_data(window)
        elif ev_name == "back":
            self._load_data(window, "back")
        elif ev_name == "initialize":
            self._load_data(window, "initialize")
        return True

    def _save_data(self, window: UnoControlDialog):
        name = cast(str, window.getModel().Name)  # type: ignore
        self._logger.debug("_save_data name: %s", name)
        if name != self._window_name:
            self._logger.debug("_save_data name not equal to window_name. Returning.")
            return
        try:
            txt_np_ver = cast("UnoControlEdit", window.getControl("txtNumpyVersion"))
            txt = txt_np_ver.getText()
            if not txt:
                txt = self._config.numpy_req  # set back to default if cleared

            txt = txt.replace(";", ",")
            txt_versions = txt.split(",")

            ver_rules = VerRules()
            matched_rules: List[str] = []
            for txt_ver in txt_versions:
                current = txt_ver.strip()
                if not current:
                    continue
                if current == "*":
                    current = "==*"
                rules = ver_rules.get_matched_rules(current)
                if not rules:
                    continue
                for rule in rules:
                    version_parts = rule.get_versions_str().split(",")
                    for part in version_parts:
                        matched_rules.append(part.strip())

            if matched_rules:
                matched_str = ", ".join(matched_rules)
                self.numpy_requirement = matched_str
                self._logger.debug("_save_data() Matched Rules: %s", matched_str)
            else:
                self._logger.error(
                    "_save_data() Invalid Numpy Requirement: '%s'. Must be in format of ==1.0.0 or >=1.0.0, <2.0.0 or ^1.0 etc.",
                    txt,
                )
                raise InvalidVersion(txt)

            settings: SettingsT = {
                "names": ("OptionLoadNumpy", "NumpyRequirement"),
                "values": (self.load_numpy, self.numpy_requirement),  # type: ignore
            }
            if self._logger.is_debug:
                self._logger.debug("_save_data() settings: %s" % settings)
            self._logger.debug(f"_save_data() settings: {settings}")
            self._config_writer(settings)
        except InvalidVersion as ver_err:
            try:
                title = self._resource_resolver.resolve_string("msg01")
                msg = self._resource_resolver.resolve_string("msg09").format(ver_err)
                _ = MessageDialog(
                    self.ctx,
                    window.getPeer(),
                    title=title,
                    message=msg,
                ).execute()
            except Exception as err:
                self._logger.error("_save_data: %s", err, exc_info=True)
        except Exception as err:
            self._logger.error("_save_data(): %s", err, exc_info=True)
            try:
                title = self._resource_resolver.resolve_string("msg01")
                msg = str(err)
                _ = MessageDialog(
                    self.ctx,
                    window.getPeer(),
                    title=title,
                    message=msg,
                ).execute()
            except Exception as err:
                self._logger.error("_save_data: %s", err, exc_info=True)
            return

        if self._has_log_options_changed():
            try:
                title = self._resource_resolver.resolve_string("msg10")
                msg = self._resource_resolver.resolve_string("msg11")
                _ = MessageDialog(
                    self.ctx,
                    window.getPeer(),
                    title=title,
                    message=msg,
                ).execute()
            except Exception as err:
                self._logger.error(
                    "OptionsDialogHandler._save_data: %s", err, exc_info=True
                )

    def get_numpy_version(self):
        from importlib.metadata import PackageNotFoundError, version

        with contextlib.suppress(PackageNotFoundError):
            return version("numpy")
        return ""

    def _load_data(self, window: UnoControlDialog, ev_name: str):
        # sourcery skip: extract-method
        name = cast(str, window.getModel().Name)  # type: ignore
        self._logger.debug("_load_data name: %s", name)
        self._logger.debug("_load_data ev_name: %s", ev_name)
        if name != self._window_name:
            return
        try:
            settings = self._settings.current_settings
            if settings:
                self.load_numpy = bool(settings["OptionLoadNumpy"])
                self.numpy_requirement = str(
                    settings.get("NumpyRequirement", self._config.numpy_req)
                )
                self._logger.debug("_load_data() Load Numpy: %s", self.load_numpy)
                self._logger.debug(
                    "_load_data() Numpy Requirement: %s", self.numpy_requirement
                )

            control_options = {
                "chkNumpy": "OptionLoadNumpy",
                "txtNumpyVersion": "NumpyRequirement",
            }
            control_values = {
                "chkNumpy": self.load_numpy,
                "txtNumpyVersion": self.numpy_requirement,
            }
            if self._logger.is_debug:
                self._logger.debug("_load_data() controls: %s", control_options)
                self._logger.debug("_load_data() control_values: %s", control_values)
            if ev_name == "initialize":
                listener = CheckBoxListener(self)
                for control in window.Controls:  # type: ignore
                    # if control.supportsService("com.sun.star.awt.UnoControlCheckBox"):
                    model = (
                        control.Model
                    )  # cast("UnoControlCheckBoxModel", control.Model)
                    if hasattr(model, "Label"):
                        if model.Name == "lblNumpyVersion":
                            res_val = self._resource_resolver.resolve_string(
                                model.Label
                            )
                            numpy_ver = self.get_numpy_version()
                            if numpy_ver:
                                model.Label = res_val.format(f"- {numpy_ver}")
                            else:
                                model.Label = res_val.format("").rstrip()
                        else:
                            model.Label = self._resource_resolver.resolve_string(
                                model.Label
                            )
                    settings_key = control_options.get(model.Name, None)
                    if not settings_key:
                        self._logger.debug(
                            "_load_data() ctl_value for %s not in dict.", model.Name
                        )
                        continue
                    self._logger.debug("_load_data() ctl_value: %s", settings_key)
                    if settings_key and control.supportsService(
                        "com.sun.star.awt.UnoControlCheckBox"
                    ):
                        model.State = self.bool_to_state(
                            settings.get(settings_key, False)
                        )
                        model.addPropertyChangeListener("State", listener)
                    elif settings_key and control.supportsService(
                        "com.sun.star.awt.UnoControlEdit"
                    ):
                        self._logger.debug(
                            "_load_data() '%s' Supports service com.sun.star.awt.UnoControlEdit",
                            model.Name,
                        )
                        txt_control = cast(
                            "UnoControlEdit", window.getControl(model.Name)
                        )
                        txt_ctl_value = control_values.get(model.Name, "")
                        self._logger.debug(
                            "_load_data() txt_ctl_value: %s", txt_ctl_value
                        )
                        txt_control.setText(txt_ctl_value)
                        if model.Name == "txtNumpyVersion":
                            model.HelpText = self._resource_resolver.resolve_string(
                                "dlgOptVerHelp"
                            )

        except Exception as err:
            self._logger.error("_load_data(): %s", err, exc_info=True)
            raise err
        return

    def state_to_bool(self, state: int) -> bool:
        return bool(state)

    def bool_to_state(self, value: bool) -> int:
        return int(value)

    def _config_writer(self, settings: SettingsT):
        try:
            cfg = Configuration()
            cfg.save_configuration(self._config_node, settings)
        except Exception as e:
            raise e

    @property
    def resource_resolver(self) -> ResourceResolver:
        return self._resource_resolver

    @property
    def load_numpy(self) -> bool:
        return self._load_numpy

    @load_numpy.setter
    def load_numpy(self, value: bool):
        self._load_numpy = value

    @property
    def numpy_requirement(self) -> str:
        return self._numpy_requirement

    @numpy_requirement.setter
    def numpy_requirement(self, value: str):
        self._numpy_requirement = value
