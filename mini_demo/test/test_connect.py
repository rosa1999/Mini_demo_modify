import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis.api_setup import StartRunProgram
from mini.dns.dns_browser import WiFiDevice

# The default log level is Warning, set to INFO
MiniSdk.set_log_level(logging.INFO)

# Before calling MiniSdk.get_device_by_name, the type of robot should be set by command MiniSdk.RobotType.EDU
# Set robot type
MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)


# Search for a robot with the robot's serial number (on the back of robot),
# the length of the serial number is arbitrary, it is recommended more than 5 characters to match exactly,
# 10 seconds timeout.
# Search results for WiFiDevice, including robot name, ip, port, etc.
async def test_get_device_by_name():
    result: WiFiDevice = await MiniSdk.get_device_by_name("00859", 10)
    print(f"test_get_device_by_name result:{result}")
    return result


# Search for the robot with the specified serial number (behind the robot's ass),
async def test_get_device_list():

    results = await MiniSdk.get_device_list(10)
    print(f"test_get_device_list results = {results}")
    return results


# MiniSdk.connect returns bool, ignoring the return value.
async def test_connect(dev: WiFiDevice):
    await MiniSdk.connect(dev)


# Enter programming mode, the robot has a tts broadcast, here through asyncio.sleep let the current concatenation
# wait for 6 seconds to return, let the robot broadcast finished.
async def test_start_run_program():
    await StartRunProgram().execute()
    await asyncio.sleep(6)
    #await MiniSdk.enter_program()


async def shutdown():
    await asyncio.sleep(1)
    #await MiniSdk.quit_program()
    await MiniSdk.release()


# The default log level is Warning, set to INFO.
MiniSdk.set_log_level(logging.INFO)
# Set robot type
MiniSdk.set_robot_type(MiniSdk.RobotType.DEDU)


async def main():
    device: WiFiDevice = await test_get_device_by_name()
    await test_connect(device)
    await test_start_run_program()
    await shutdown()


if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
