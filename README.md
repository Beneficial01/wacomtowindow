# Wacom Window Mapper

A Python script that allows you to easily map your Wacom tablet to a specific window on Linux. It automatically detects your Wacom devices and lets you choose which window to map to, using precise window geometry for accurate mapping.

## Features

- Automatic detection of Wacom devices (pen and eraser)
- Lists all available windows with their precise geometry

## Prerequisites

- Python 3
- `xsetwacom` (usually comes with Wacom drivers)
- `wmctrl` (install with `sudo apt-get install wmctrl` on Ubuntu/Debian)
- `xwininfo` (install with `sudo apt-get install x11-utils` on Ubuntu/Debian)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Beneficial01/wacomtowindow
cd wacomtowindow
```

2. Make the script executable:
```bash
chmod +x wacomtowindow.py
```

## Usage

### Direct Usage
Simply run the script:
```bash
./wacomtowindow.py
```

### Keyboard Shortcut (GNOME)
1. Open Settings → Keyboard → Keyboard Shortcuts
2. Add a custom shortcut
3. Set the command to:
```bash
gnome-terminal -- /full/path/to/wacomtowindow.py
```
4. Assign your preferred keyboard shortcut (e.g., Ctrl+Alt+W)

## How It Works

1. The script first detects all connected Wacom devices (pen and eraser)
2. It then lists all open windows with their precise geometry
3. You select which window you want to map to using the number keys
4. The script automatically maps both pen and eraser to the selected window using the most accurate geometry available

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

MIT License