# dl120th_logger/dl120th/logger.py

import sys
from datetime import datetime, timedelta
from struct import unpack
import usb1

from .device import DeviceDescriptor


class Dl120th:
    """
    Class to interact with Voltcraft DL-120TH data logger.
    This tool is used to record temperatures and relative humidity.
    """
    VENDOR_ID = 0x10C4
    PRODUCT_ID = 0x0003
    INTERFACE_ID = 0
    BULK_IN_EP = 0x81
    BULK_OUT_EP = 0x02
    PACKET_LENGTH = 0x40

    num_data = 0
    temp = []
    rh = []

    device_descriptor = DeviceDescriptor(VENDOR_ID, PRODUCT_ID, INTERFACE_ID)

    def __init__(self):
        """Initialize the data logger and prepare internal state."""
        self.device = self.device_descriptor.get_device()
        self.handle = None
        self.status = (0, 0, 0, 0)

    def open(self):
        """
        Open and claim the USB interface to communicate with the device.
        Exits if device is not found or interface cannot be claimed.
        """
        self.device = self.device_descriptor.get_device()
        if not self.device:
            print("Device isn't plugged in.")
            sys.exit(1)

        try:
            self.handle = self.device.open()
            self.handle.claimInterface(
                self.device_descriptor.interface_id
            )
        except usb1.USBError as err:
            print("Error while opening USB device:", err)
            sys.exit(1)

    def close(self):
        """Release the USB interface and reset internal handle/device state."""
        try:
            self.handle.reset()
            self.handle.releaseInterface()
        except Exception as err:
            print("Error while closing USB device:", err)

        self.handle, self.device = None, None

    def read_config(self):
        """
        Send command to read the logger configuration.
        Parses data including start time, interval,
        logger name, thresholds, etc.
        """
        msg = [0x00, 0x10, 0x01]
        sent_bytes = self.handle.bulkWrite(
            self.BULK_OUT_EP, bytes(msg), 1000
        )
        print("Read Config request return:", sent_bytes)

        if sent_bytes:
            read_bytes = self.handle.bulkRead(
                self.BULK_IN_EP, self.PACKET_LENGTH, 1000
            )

        print("Read Config response return:", read_bytes)

        data = self.handle.bulkRead(
            self.BULK_IN_EP, self.PACKET_LENGTH, 1000
        )
        print("Config data:", data)

        unpacked = unpack(
            "IIIIIhhhhBBBBBBB16sBhhhhI", bytes(data)
        )

        (
            self.logger_state,
            self.num_data_conf,
            self.num_data_rec,
            self.interval,
            start_year,
            _,
            self.thresh_temp_low,
            _,
            self.thresh_temp_high,
            start_month,
            start_mday,
            start_hour,
            start_min,
            start_sec,
            self.temp_fahrenheit,
            self.led_conf,
            self.logger_name,
            self.logger_start,
            _,
            self.thresh_rh_low,
            _,
            self.thresh_rh_high,
            self.logger_end
        ) = unpacked

        self.start_rec = datetime(
            start_year, start_month, start_mday,
            start_hour, start_min, start_sec
        )
        duration = self.num_data_rec * self.interval
        self.end_rec = self.start_rec + timedelta(seconds=duration)
        self.logger_name = self.logger_name.replace(b'\x00', b'').decode()

    def read_data(self):
        """
        Read recorded temperature and humidity data from the device.
        Populates the temp and rh lists with raw sensor data.
        """
        print("Reading logged measurement data...")

        self.temp = []
        self.rh = []

        num_records = self.num_data_rec
        record_size = 4
        total_bytes = num_records * record_size
        bytes_read = 0

        while bytes_read < total_bytes:
            try:
                chunk = self.handle.bulkRead(
                    self.BULK_IN_EP, self.PACKET_LENGTH, timeout=1000
                )
                bytes_read += len(chunk)

                for i in range(0, len(chunk), 4):
                    if i + 3 < len(chunk):
                        temp_raw = unpack('<h', chunk[i:i + 2])[0]
                        rh_raw = unpack('<h', chunk[i + 2:i + 4])[0]
                        self.temp.append(temp_raw)
                        self.rh.append(rh_raw)
            except usb1.USBErrorTimeout:
                print("Timeout while reading measurement data.")
                break

        print(
            f"✅ Read {len(self.temp)} temperature and "
            f"{len(self.rh)} humidity values."
        )

    def print_data(self):
        """
        Print all collected temperature and
        humidity values in human-readable form.
        Values are divided by 10 to represent
        degrees Celsius and relative humidity %.
        """
        for i in range(self.num_data_rec):
            print(
                self.temp[i] / 10.0,
                "°C",
                self.rh[i] / 10.0,
                "%RH"
            )
