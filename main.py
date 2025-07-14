import asyncio
from bleak import BleakClient
from device_scanner import find_govee_devices_async

GOVEE_COMMAND_UUID = "00010203-0405-0607-0809-0a0b0c0d2b11"
POWER_ON = bytearray([0x33, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x33])
POWER_OFF = bytearray([0x33, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x32])

async def control_all_devices():
    devices = await find_govee_devices_async()
    
    if not devices:
        print("No Govee devices found!")
        return
    
    print(f"found {len(devices)} devices")
    
    for address, name in devices.items():
        print(f"connecting to {name}...")
        
        async with BleakClient(address) as client:
            print("turning ON...")
            await client.write_gatt_char(GOVEE_COMMAND_UUID, POWER_ON)
            
            await asyncio.sleep(5)
            
            print("turning OFF...")
            await client.write_gatt_char(GOVEE_COMMAND_UUID, POWER_OFF)
            
            print(f"done with {name}")

if __name__ == "__main__":
    asyncio.run(control_all_devices())