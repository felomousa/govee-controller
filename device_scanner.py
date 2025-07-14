import asyncio
from bleak import BleakScanner

async def find_govee_devices_async(scan_duration=10):
    return await _scan_for_govee(scan_duration)

async def _scan_for_govee(scan_duration):
    devices = {}
    
    def device_found(device, advertisement_data):
        name = device.name or advertisement_data.local_name or "Unknown Device"
        if "govee" in name.lower():
            devices[device.address] = name
    
    scanner = BleakScanner(device_found)
    await scanner.start()
    await asyncio.sleep(scan_duration)
    await scanner.stop()
    
    return devices