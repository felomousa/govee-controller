import asyncio
from goveeHelper import find_govee_devices_async, GoveeCommand, control_single_device

async def control_all_devices():
    devices = await find_govee_devices_async()
    cmd = GoveeCommand()
    
    if not devices:
        print("no Govee devices found")
        return
    
    print(f"found {len(devices)} devices")
    
    tasks = [control_single_device(device, name, cmd) for device, name in devices.items()]
    await asyncio.gather(*tasks)
    
    print("all devices controlled!")

if __name__ == "__main__":
    asyncio.run(control_all_devices())