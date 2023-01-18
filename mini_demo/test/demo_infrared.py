import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis.api_observe import ObserveInfraredDistance
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observeinfrareddistance_pb2 import ObserveInfraredDistanceResponse
from test.test_connect import test_connect, test_start_run_program, shutdown
from test.test_connect import test_get_device_by_name


async def test_ObserveInfraredDistance():
    """Monitor infrared distance demo

    Listen for infrared distance events,
    and the robot reports the detected infrared distance to the nearest obstacle in front of it

    When the returned infrared distance is less than 500,
    stop listening and broadcast "Detected infrared distance xxx" (xxx is the infrared distance value)

    """
    # Infrared monitoring of objects
    observer: ObserveInfraredDistance = ObserveInfraredDistance()

    # Defining the Processor
    # ObserveInfraredDistanceResponse.distance
    def handler(msg: ObserveInfraredDistanceResponse):
        print("distance = {0}".format(str(msg.distance)))
        if msg.distance < 500:
            observer.stop()
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    result = await StartPlayTTS(text="Is someone there, who are you").execute()
    print(f"tts over {result}")
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


async def main():
    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_ObserveInfraredDistance()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
