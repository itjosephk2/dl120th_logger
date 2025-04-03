# DL120TH Logger 

A Python tool to interface with the **Voltcraft DL-120TH** USB temperature and humidity logger. This project allows you to read configuration settings from the device and download logged environmental data directly via USB using the `usb1` library.

---

## Features

- Read configuration details like interval, start time, and thresholds
- Retrieve and print recorded temperature and humidity data
- USB communication via Python and libusb1
- Modular code following PEP8 with clean docstrings

---

## Requirements

- Python 3.8+
- [libusb1](https://pypi.org/project/libusb1/) Python bindings

### Install dependencies:

```bash
pip install libusb1
```

---

## Project Structure

```
dl120th_logger/
├── dl120th/
│   ├── __init__.py           # Marks this as a package
│   ├── device.py             # USB device descriptor class
│   └── logger.py             # Main class for interacting with the DL-120TH
├── main.py                   # (Optional) CLI entry point
└── README.md                 # You're reading it!
```

---

##  Example Usage


---

## Development Notes



---

## To Do / Roadmap

- [ ] CLI tool for config, download, and export
- [ ] Save data to CSV or SQLite
- [ ] Exception handling improvements
- [ ] Real-time reading (if supported by device)

---

## Author

**Joseph K.**  
GitHub: [@itjosephk2](https://github.com/itjosephk2)

---

## License

This project is open-source and available under the MIT License. Feel free to use, modify, and contribute!
