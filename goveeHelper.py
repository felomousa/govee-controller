import asyncio
from bleak import BleakScanner, BleakClient

GOVEE_COMMAND_UUID = "00010203-0405-0607-0809-0a0b0c0d2b11"

async def find_govee_devices_async(scan_duration=1):
    return await _scan_for_govee(scan_duration)

async def _scan_for_govee(scan_duration):
    devices = {}
    
    def device_found(device, advertisement_data):
        name = device.name or advertisement_data.local_name or "Unknown Device"
        if "govee" in name.lower():
            devices[device] = name
    
    scanner = BleakScanner(device_found)
    await scanner.start()
    await asyncio.sleep(scan_duration)
    await scanner.stop()
    
    return devices

class GoveeCommand:
    def __init__(self):
        self.header = 0x33
        self.padding = [0x00] * 16
    
    def _build_command(self, cmd_type, *data):
        cmd = bytearray([self.header, cmd_type, *data, *self.padding]) 
        cmd = cmd[:19]
        checksum = 0
        for b in cmd:
            checksum ^= b
        cmd.append(checksum)
        return cmd
    
    def power(self, on=True):
        return self._build_command(0x01, 0x01 if on else 0x00)
    
    def brightness(self, level):  # 1-100
        value = int(0x14 + (level - 1) * (0xFE - 0x14) / 99)
        return self._build_command(0x04, value)
    
    def color(self, r, g, b):  # RGB(0,255)
        return self._build_command(0x05, 0x02, r, g, b)
    
async def control_single_device(device, name, cmd):
    print(f"connecting to {name}...")
    
    async with BleakClient(device) as client: 
        print(f"{name}: turning ON...")
        await client.write_gatt_char(GOVEE_COMMAND_UUID, cmd.power(True))
        
        await asyncio.sleep(2)
        
        print(f"{name}: setting to red...")
        await client.write_gatt_char(GOVEE_COMMAND_UUID, cmd.color(255, 0, 0))
        
        await asyncio.sleep(2)
        
        print(f"{name}: dimming to 30%...")
        await client.write_gatt_char(GOVEE_COMMAND_UUID, cmd.brightness(30))
        
        await asyncio.sleep(3)
        
        await client.write_gatt_char(GOVEE_COMMAND_UUID, cmd.power(False))
        
        print(f"done with {name}")
