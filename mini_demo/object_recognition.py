import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis import errors
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.apis.api_sence import ObjectRecognise, ObjectRecogniseType
from test.test_connect import test_connect
from test.test_connect import test_get_device_by_name


# Test object recognition: identify fruit, 10s timeout
async def test_object_recognise_fruit():
    """
    Test object (fruit) recognition
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE objects.
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FRUIT, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    return response.objects
    # print(f'test_object_recognise_fruit result: {response}')


# Test object recognition: gesture recognition, 10s timeout
async def test_object_recognise_gesture():
    """
    test object (gesture) recognition
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.GESTURE, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    return response.objects
    # print(f'test_object_recognise_gesture result: {response}')


async def test_play_ts():
    """
    test_play_tts
    Make the robot start playing a tts saying "Show me an item" and wait for the result.
    #ControlTTSResponse.isSuccess : if successful
    #ControlTTSResponse.resultCode : return code
    """
    # is_serial:serial execution
    # text: the text to combine
    block: StartPlayTTS = StartPlayTTS(text="Show me an item")
    # Returns a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block response contains resultCode and isSuccess
    # If resultCode ! =0 can be queried by errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))


async def test_object_recognise_all():
    """
    Test object (all) recognition
    Have the robot identify all, time out for 10s, and wait for the results
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.ALL, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    return response.objects
    # print(f'test_object_recognise_all result: {response}')


async def _ts(name):
    block: StartPlayTTS = StartPlayTTS(text=f'There is {name}')
    response = await block.execute()
    print(f'test_object_recognise result: {response}')


async def test_object_recognise_flower():
    """
    Test object (flower) recognition
    Have the robot identify the flower
    (you have to manually put the flower or a photo of the flower in front of the robot), time out for 10s,
    and wait for the results
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    return response.objects
    # print(f'test_object_recognise_flower result: {response}')


async def main():
    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    
    await test_play_ts()
    result = await test_object_recognise_all()
    await _ts(result)
    await asyncio.sleep(5)
    await test_play_ts()
    result1 = await test_object_recognise_fruit()
    await _ts(result1)
    await asyncio.sleep(5)
    await test_play_ts()
    result2 = await test_object_recognise_gesture()
    await _ts(result2)
    await test_play_ts()
    result3 = await test_object_recognise_flower()
    await _ts(result3)
    

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
