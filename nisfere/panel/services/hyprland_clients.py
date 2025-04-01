import json
from loguru import logger
from typing import Optional

from fabric.core.service import Service, Signal, Property
from fabric.hyprland.service import Hyprland
from fabric.hyprland.widgets import get_hyprland_connection

from fabric.utils.helpers import bulk_connect


class HyprlandClient(Service):

    @Signal
    def changed(self) -> None: ...

    @Signal
    def closed(self) -> None: ...

    @Property(str, flags="readable")
    def address(self) -> str:
        return self._client_data.get("address", "")

    @Property(str, flags="readable")
    def title(self) -> str:
        return self._client_data.get("title", "Unknown")

    @Property(str, flags="readable")
    def class_name(self) -> str:
        return self._client_data.get("class", "Unknown").lower()

    @Property(int, flags="readable")
    def workspace(self) -> int:
        return self._client_data.get("workspace", {}).get("id", -1)

    @Property(Optional[int], flags="readable")
    def pid(self) -> Optional[int]:
        return self._client_data.get("pid")

    @Property(bool, flags="readable", default_value=False)
    def floating(self) -> bool:
        return self._client_data.get("floating", False)

    @Property(bool, flags="read-write", default_value=False)
    def focused(self) -> bool:
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        self._focused = value
        self.changed.emit()

    def __init__(self, client_data: dict):
        super().__init__()
        self._client_data = client_data
        self._focused = client_data.get("focusHistoryID", 1) == 0

    def update(self, client_data: dict):
        self._client_data = client_data
        self._focused = client_data.get("focusHistoryID", 1) == 0
        self.changed.emit()

    def close(self):
        self.closed.emit()

    def __repr__(self):
        return f"<HyprlandClient {self.title} ({self.class_name}) on {self.workspace}>"


class HyprlandClients(Service):
    """Clients service to detect the active client"""

    @Signal
    def initialized(self) -> None: ...

    @Signal
    def client_removed(self, client: HyprlandClient) -> None: ...

    @Signal
    def client_added(self, client: HyprlandClient) -> None: ...

    @Signal
    def empty_workspace(self) -> None: ...

    @Signal
    def filled_workspace(self) -> None: ...

    @Property(list, flags="readable")
    def clients(self) -> list:
        return self._clients.values()

    def __init__(self):
        super().__init__()
        self._connection: Hyprland = get_hyprland_connection()
        self._clients: dict[str, HyprlandClient] = {}
        # Now stores HyprlandClient instance
        self._active_client: Optional[HyprlandClient] = None

        if self._connection.ready:
            self._initialize()
        else:
            self._connection.connect(
                "event::ready", lambda *args:  self._initialize())

        bulk_connect(
            self._connection,
            {
                "event::activewindow": lambda *args: self._get_hypr_clients(),
                # "event::closewindow": lambda *args: self._get_hypr_clients(),
                # "event::workspace": lambda *args: self._check_workspace()
            }
        )

    def _initialize(self):
        raw_clients = json.loads(
            self._connection.send_command("j/clients").reply.decode())

        for client_data in raw_clients:
            new_client = HyprlandClient(client_data)
            self._clients[new_client.address] = new_client

        self.initialized.emit()

        self.empty_workspace.emit() if len(
            self._clients) == 0 else self.filled_workspace.emit()

        logger.info(
            f"[Dock] Loaded {len(self._clients)} clients: {list(self._clients.values())}")

    def _get_hypr_clients(self):

        raw_clients = json.loads(
            self._connection.send_command("j/clients").reply.decode())

        new_clients = {c["address"]: c for c in raw_clients}

        # Find removed clients
        removed_clients = set(self._clients.keys()) - set(new_clients.keys())
        for removed in removed_clients:
            removed_client = self._clients.pop(removed, None)
            if removed_client:
                removed_client.close()  # Emit closed signal
                self.client_removed.emit(removed_client)
                logger.info(f"[Dock] Client removed: {removed_client}")

        # Check for added and updated clients
        for address, client_data in new_clients.items():
            if address not in self._clients:
                # New client detected
                new_client = HyprlandClient(client_data)
                self._clients[address] = new_client
                self.client_added.emit(new_client)
                logger.info(
                    f"[Dock] New client added: {new_client.class_name}")
            else:
                # Existing client, update data
                existing_client = self._clients[address]
                existing_client.update(client_data)

        self._check_workspace()

        logger.info(f"[Dock] Updated {len(self._clients)} clients")

    def _check_workspace(self):
        current_ws = json.loads(self._connection.send_command(
            "j/activeworkspace").reply.decode()).get("id", 0)

        # if a client is inside the current workspace emit the filled signal
        if any(ws.workspace == current_ws for ws in self._clients.values()):
            self.filled_workspace.emit()
        # if not client found, find the current focused client and change the focused value to False, also emit the empty signal
        else:
            if (focused_client := self._get_focused_client()):
                focused_client.focused = False
            self.empty_workspace.emit()

    def _get_focused_client(self) -> Optional[HyprlandClient]:
        return next((client for client in self._clients.values() if client.focused), None)
