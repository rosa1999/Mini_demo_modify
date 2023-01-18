import asyncio
import logging

import mini.mini_sdk as MiniSdk

from mini.apis.api_observe import ObserveRobotPosture, RobotPosture
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_observefallclimb_pb2 import ObserveFallClimbResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# Test, attitude detection
async def test_ObserveRobotPosture():
    # Event handler
    # ObserveFallClimbResponse.status
    # STAND = 1; //Stand
    # SPLITS_LEFT = 2; //Left lunge
    # SPLITS_RIGHT = 3; //Right lunge
    # SITDOWN = 4; //Sit down
    # SQUATDOWN = 5; //Squat down
    # KNEELING = 6; //Kneel down
    # LYING = 7; //Lying on your side
    # LYINGDOWN = 8; //Lying down
    # SPLITS_LEFT_1 = 9; //Left split
    # SPLITS_RIGHT_2 = 10;//right split
    # BEND = 11;//Bent over

    # Create listening object
    observer: ObserveRobotPosture = ObserveRobotPosture()

    def handler(msg: ObserveFallClimbResponse):
        print("{0}".format(msg))
        if msg.status == 8 or msg.status == 7:
        #if msg.status == RobotPosture.LYING.value or msg.status == RobotPosture.LYING_DOWN.value:
            observer.stop()
            asyncio.create_task(__tts())

    observer.set_handler(handler)
    # start
    observer.start()
    await asyncio.sleep(0)


async def __tts():
    await StartPlayTTS(text="I fell down").execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_ObserveRobotPosture()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
