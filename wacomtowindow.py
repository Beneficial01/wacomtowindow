#!/usr/bin/env python3
import subprocess
import re
from typing import Dict, List, Tuple
import sys

def get_wacom_devices() -> Dict[str, str]:
    """Get Wacom devices and their IDs."""
    try:
        output = subprocess.check_output(['xsetwacom', '--list', 'devices']).decode()
        devices = {}
        for line in output.splitlines():
            if 'type: STYLUS' in line or 'type: ERASER' in line:
                name = line.split('\t')[0].strip()
                id_match = re.search(r'id:\s*(\d+)', line)
                if id_match:
                    devices[name] = id_match.group(1)
        return devices
    except subprocess.CalledProcessError:
        print("Error: Unable to get Wacom devices. Make sure xsetwacom is installed.")
        sys.exit(1)

def get_window_geometry(window_id: str) -> str:
    """Get precise window geometry using xwininfo."""
    try:
        output = subprocess.check_output(['xwininfo', '-id', window_id]).decode()
        
        # Extract dimensions and position
        width = re.search(r'Width: (\d+)', output)
        height = re.search(r'Height: (\d+)', output)
        geometry = re.search(r'-geometry (\d+x\d+[+-]\d+[+-]\d+)', output)
        
        if geometry:
            return geometry.group(1)
        elif width and height:
            # Fallback to parsing individual components
            x = re.search(r'Absolute upper-left X:\s+(\d+)', output)
            y = re.search(r'Absolute upper-left Y:\s+(\d+)', output)
            if x and y:
                return f"{width.group(1)}x{height.group(1)}+{x.group(1)}+{y.group(1)}"
        
        raise ValueError("Could not parse window geometry")
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error getting precise window geometry: {e}")
        return None

def get_windows() -> List[Tuple[str, str, str]]:
    """Get list of windows with their IDs and titles."""
    try:
        output = subprocess.check_output(['wmctrl', '-lG']).decode()
        windows = []
        for line in output.splitlines():
            parts = line.split(None, 7)  # Split by whitespace, max 8 parts
            if len(parts) >= 8:
                window_id = parts[0]
                title = parts[7]
                # Get precise geometry using xwininfo
                geometry = get_window_geometry(window_id)
                if geometry:
                    windows.append((title, geometry, window_id))
        return windows
    except subprocess.CalledProcessError:
        print("Error: Unable to get window list. Make sure wmctrl is installed.")
        sys.exit(1)

def map_wacom_to_window(device_ids: List[str], geometry: str):
    """Map Wacom devices to specified window geometry."""
    for device_id in device_ids:
        try:
            subprocess.run(['xsetwacom', '--set', device_id, 'MapToOutput', geometry], check=True)
            print(f"Successfully mapped device {device_id} to {geometry}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to map device {device_id}")

def main():
    # Get Wacom devices
    devices = get_wacom_devices()
    if not devices:
        print("No Wacom devices found.")
        return

    print("Found Wacom devices:")
    for name, device_id in devices.items():
        print(f"- {name} (ID: {device_id})")

    # Get windows with precise geometry
    windows = get_windows()
    if not windows:
        print("No windows found.")
        return

    print("\nAvailable windows:")
    for i, (title, geometry, _) in enumerate(windows, 1):
        print(f"{i}. {title}")
        print(f"   Geometry: {geometry}")

    # Get user selection
    while True:
        try:
            choice = int(input("\nSelect window number to map to (or 0 to exit): "))
            if choice == 0:
                return
            if 1 <= choice <= len(windows):
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    selected_window = windows[choice - 1]
    print(f"\nMapping to window: {selected_window[0]}")
    print(f"Using geometry: {selected_window[1]}")

    # Map all devices to the selected window
    map_wacom_to_window(list(devices.values()), selected_window[1])

if __name__ == "__main__":
    main()