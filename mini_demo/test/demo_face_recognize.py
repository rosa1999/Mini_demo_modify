import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis.api_observe import ObserveFaceRecognise, ObserveFaceDetect
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facedetecttask_pb2 import FaceDetectTaskResponse
from mini.pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# Test, if the registered face is detected, the incident will be reported, if it is a stranger,
# it will return to "stranger"
async def test_ObserveFaceRecognise():
    """
    Face recognition demo

    Listen to face recognition events, and the robot reports the recognized face information (array)

    If it is a registered face, return face details: id, name, gender, age

    If it is a stranger, return name: "stranger"

    When the face is successfully recognized,
    stop listening and broadcast "Hello, xxx" (xxx is the name in the face information)

    """
    observer: ObserveFaceRecognise = ObserveFaceRecognise()

    # FaceRecogniseTaskResponse.faceInfos: [FaceInfoResponse]
    # FaceInfoResponse.id, FaceInfoResponse.name,FaceInfoResponse.gender,FaceInfoResponse.age
    # FaceRecogniseTaskResponse.isSuccess
    # FaceRecogniseTaskResponse.resultCode
    def handler(msg: FaceRecogniseTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.faceInfos:
            observer.stop()
            asyncio.create_task(__tts(msg.faceInfos[0].name))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(name):
    await PlayTTS(text=f'Hello， {name}').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


# Face detection, if a face is detected, the incident will be reported
async def test_ObserveFaceDetect():
    observer: ObserveFaceDetect = ObserveFaceDetect()

    # FaceDetectTaskResponse.count
    # FaceDetectTaskResponse.isSuccess
    # FaceDetectTaskResponse.resultCode
    def handler(msg: FaceDetectTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.count:
            observer.stop()
            asyncio.create_task(__tts(msg.count))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(count):
    await PlayTTS(text=f'There seems to be {count} people in front of me').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_ObserveFaceRecognise()
    await test_ObserveFaceDetect()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
