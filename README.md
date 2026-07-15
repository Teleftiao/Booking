# Hotel Booking App - Executable Setup

## Quick Start

### Option 1: One-Click Launcher (Recommended)
Double-click: **`launcher.bat`**
- Installs dependencies automatically if needed
- Launches the app in your browser at `http://localhost:8501`

### Option 2: Setup and Run
Double-click: **`setup_and_run.bat`**
- Installs all required packages
- Starts the Streamlit server

### Option 3: Build Standalone Executable
Double-click: **`build_executable.bat`**
- Creates a standalone `HotelBookingApp.exe` in the `dist` folder
- No Python installation needed to run the .exe
- Run the .exe directly after building

## Requirements
- Python 3.8+ installed (add to PATH during installation)
- Internet connection for first run (to download dependencies)

## Troubleshooting

**"Python is not installed":**
- Download from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

**Port 8501 already in use:**
- The app will try to use the next available port (8502, 8503, etc.)

**Streamlit not starting:**
- Run `setup_and_run.bat` to reinstall dependencies

## File Structure
```
Booking/
├── launcher.bat                 # One-click launcher (use this!)
├── setup_and_run.bat           # Manual setup
├── build_executable.bat        # Build standalone .exe
├── app.py                      # Main application
├── requirement.txt             # Python dependencies
├── data_inventaris.csv         # Inventory data
├── data_transaksi.csv          # Transaction ledger
├── data_booking.csv            # Booking records
└── data_kamar.csv              # Room data
```

## Created Launchers

1. **launcher.bat** - Simple one-click launcher
2. **setup_and_run.bat** - Setup dependencies then run
3. **build_executable.bat** - Create a standalone .exe (requires PyInstaller)

Just double-click any `.bat` file to start!
