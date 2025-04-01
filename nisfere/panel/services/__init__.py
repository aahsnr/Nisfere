from services.media_player import MediaPlayer as MediaPlayerService, MediaManager
from services.hyprland_language import HyprlandLanguage
from services.notifications import Notifications,  Notification, CachedNotification, CachedNotifications
from services.hyprland_clients import HyprlandClients, HyprlandClient
from services.screenshot import Screenshot
from services.screen_recorder import ScreenRecorder
from services.network_manager import NetworkClient, Wifi, Ethernet, AccessPoint
from services.battery import Battery
from services.brightness import Brightness
from fabric.audio import Audio
from fabric.bluetooth import BluetoothClient

notification_service = CachedNotifications()

hyprland_language_service = HyprlandLanguage()

hyprland_clients_service = HyprlandClients()

audio_service = Audio()

network_manager_service = NetworkClient()

screenshot_service = Screenshot()

screen_recorder_service = ScreenRecorder()

battery_service = Battery()

brightness_service = Brightness()

bluetooth_service = BluetoothClient()