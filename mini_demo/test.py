import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice


async def test_get_device_by_name():
    result: WiFiDevice = await MiniSdk.get_device_by_name("00859", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


async def main():

    await test_get_device_by_name()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
