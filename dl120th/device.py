import usb1


class DeviceDescriptor:
    """
    Represents a USB device descriptor for identifying and accessing
    a specific USB device by its vendor ID and product ID.
    """

    def __init__(self, vendor_id, product_id, interface_id):
        """
        Initialize the descriptor with vendor, product, and interface IDs.

        :param vendor_id: USB vendor ID of the device
        :param product_id: USB product ID of the device
        :param interface_id: Interface number to use
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_id = interface_id

    def get_device(self):
        """
        Search for a connected USB device matching the vendor and product ID.

        :return: Matching USB device object or None if not found
        """
        context = usb1.USBContext()
        for device in context.getDeviceList():
            if (
                device.getVendorID() == self.vendor_id
                and device.getProductID() == self.product_id
            ):
                return device
        return None
    