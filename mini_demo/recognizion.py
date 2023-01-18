import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis import errors
from mini.apis.api_sence import FaceAnalysis, ObjectRecognise, ObjectRecogniseType
from mini.apis.api_observe import ObserveFaceRecognise, ObserveFaceDetect
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facedetecttask_pb2 import FaceDetectTaskResponse
from mini.pb2.codemao_facerecognisetask_pb2 import FaceRecogniseTaskResponse
from mini.apis.api_expression import PlayExpression

from test.test_connect import test_connect
from test.test_connect import test_get_device_by_name


async def test_play_tts():
    """
    test_play_tts
    Make the robot start playing a tts saying "Let yourself be recognized?" and wait for the result.
    #ControlTTSResponse.isSuccess : if successful
    #ControlTTSResponse.resultCode : return code
    """
    # is_serial:serial execution
    # text: the text to combine
    block: StartPlayTTS = StartPlayTTS(text="Let yourself be recognized?")
    # Returns a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block response contains resultCode and isSuccess
    # If resultCode ! =0 can be queried by errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))


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
            asyncio.create_task(_tts(msg.faceInfos[0].name))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(5)


async def _tts(name):
    block: StartPlayTTS = StartPlayTTS(text=f'Hello, {name}')
    response = await block.execute()
    print(f'test_ObserveFaceRecognise: {response}')


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
    await asyncio.sleep(5)


async def __tts(count):
    block: StartPlayTTS = StartPlayTTS(text=f'There seems to be {count} people in front of me')
    response = await block.execute()
    print(f'test_ObserveFaceDetect: {response}')



# Test face analysis (gender)
async def test_face_analysis():
    """
    Test face analysis (gender)

    Detect face information (gender, age), timeout 10s, and wait for the reply result

    When multiple people exist in front of the camera,
    return the face information with the largest proportion of the screen

    Return value: Example {"age": 24, "gender": 99, "height": 238, "width": 238}

    age: age

    gender: [1, 100], less than 50 is female, greater than 50 is male

    height: the height of the face in the camera image

    width: the width of the face in the camera screen

    """
    block: FaceAnalysis = FaceAnalysis(timeout=10)
    # response: FaceAnalyzeResponse
    (resultType, response) = await block.execute()

    # print(f'test_face_analysis result: {response}')
    print('code = {0}, error={1}'.format(response.resultCode, errors.get_vision_error_str(response.resultCode)))
    return response.faceInfos[0].age


async def _ts(name):
    block: StartPlayTTS = StartPlayTTS(text=f'The age is {name}')
    response = await block.execute()
    print(f'test_face_analysis result: {response}')


async def test_play_ts():
    """
    test_play_tts
    Make the robot start playing a tts saying "See how my eyes change" and wait for the result.
    #ControlTTSResponse.isSuccess : if successful
    #ControlTTSResponse.resultCode : return code
    """
    # is_serial:serial execution
    # text: the text to combine
    block: StartPlayTTS = StartPlayTTS(text="See how my eyes change")
    # Returns a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block response contains resultCode and isSuccess
    # If resultCode ! =0 can be queried by errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))


# function that allows you to change the eyes of the robot
async def test_play_expression():
    """
    Test play expressions
    Let the bot play a built-in emoticon called "codemao19" and wait for the reply results!
    #PlayExpressionResponse.isSuccess : Success or not
    #PlayExpressionResponse.resultCode : Return Code
    """

    block: PlayExpression = PlayExpression(express_name="codemao19")
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')



async def main():
    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)


    await test_play_tts()
    await test_ObserveFaceRecognise()
    await test_ObserveFaceDetect()
    await asyncio.sleep(2)
    result = await test_face_analysis()
    await _ts(result)
    await asyncio.sleep(2)
    await test_play_ts()
    await test_play_expression()


if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
