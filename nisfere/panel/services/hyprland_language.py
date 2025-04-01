import re
import json
from loguru import logger

from fabric.core.service import Service, Signal, Property
from fabric.utils.helpers import FormattedString
from fabric.hyprland.service import Hyprland, HyprlandEvent

from fabric.hyprland.widgets import get_hyprland_connection
from utils.config import CONFIG


class HyprlandLanguage(Service):
    """Language service to detect the active keyboard layout"""

    @Signal
    def language_changed(self, lang: str) -> None:
        """Signal emitted when the language changes (e.g., us, gr)"""
        pass

    @Property(str, flags="readable")
    def language(self) -> str:
        return self._language

    def __init__(self, keyboard=".*"):
        super().__init__()
        self._connection: Hyprland = get_hyprland_connection()
        self._keyboard = keyboard
        self._formatter: FormattedString = FormattedString(
            string="{get_language(language)}",
            get_language=lambda language: CONFIG['keyboard_layouts'][language]
        )

        self._language = ""

        if self._connection.ready:
            self._get_active_language()
        else:
            self._connection.connect("event::ready", self._get_active_language)

        self._connection.connect("event::activelayout", self._on_activelayout)

    def _get_active_language(self, *_):
        devices: dict[str, list[dict[str, str]]] = json.loads(
            str(self._connection.send_command("j/devices").reply.decode())
        )
        if not devices or not (keyboards := devices.get("keyboards")):
            return logger.warning(
                f"[Language] cound't get devices from hyprctl, gotten data\n{devices}"
            )

        language: str | None = None
        for kb in keyboards:
            if (
                not (kb_name := kb.get("name"))
                or not re.match(self._keyboard, kb_name)
                or not kb.get("main")
                or not (language := kb.get("active_keymap"))
            ):
                continue
            self._language = self._formatter.format(language=language)
            self.language_changed.emit(
                self._formatter.format(language=language))

            logger.debug(
                f"[Language] found language: {language} for keyboard {kb_name}"
            )
            break

        return (
            logger.info(
                f"[Language] Could not find language for keyboard: {self._keyboard}, gotten keyboards: {keyboards}"
            )
            if not language
            else logger.info(
                f"[Language] Set language: {language} for keyboard: {self._keyboard}"
            )
        )

    def _on_activelayout(self, _, event: HyprlandEvent):
        if len(event.data) < 2:
            return logger.warning(
                f"[Language] got invalid event data from hyprland, raw data is\n{event.raw_data}"
            )
        keyboard, language = event.data
        matched: bool = False

        if re.match(self._keyboard, keyboard) and (matched := True):
            self._language = self._formatter.format(language=language)
            self.language_changed.emit(
                self._formatter.format(language=language))
        return logger.debug(
            f"[Languag/e] Keyboard: {keyboard}, Language: {language}, Match: {matched}"
        )

    def change_language(self):
        self._connection.send_command("switchxkblayout current next")
