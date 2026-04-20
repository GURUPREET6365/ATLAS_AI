import subprocess
from ATLAS_API.app.telegram.utilities.send_message import send_message


def set_battery_mode(mode):
    #  powerprofilesctl set power-saver, balanced, or performance

    cmd=['powerprofilesctl', 'set', f'{mode}']
    