import asyncio
import logging


from mini.apis import errors
from mini.apis.api_sound import StartPlayTTS
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sence import TakePicture, TakePictureResponse, TakePictureType
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect
from test.test_connect import test_get_device_by_name
import mini.mini_sdk as MiniSdk


async def test_play_tts():
    """
    test_play_tts
    Make the robot start playing a tts saying "Hello, I'm AlphaMini, what's your name?" and wait for the result.
    #ControlTTSResponse.isSuccess : if successful
    #ControlTTSResponse.resultCode : return code
    """
    # is_serial:serial execution
    # text: the text to combine
    block: StartPlayTTS = StartPlayTTS(text="Hello, I'm AlphaMini, what's your name?")
    # Returns a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block response contains resultCode and isSuccess
    # If resultCode ! =0 can be queried by errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))



async def __tts(name):
    block: StartPlayTTS = StartPlayTTS(text=f'Hello {name} nice to meet you. Can i take a picture for remember you in the future?')
    response = await block.execute()
    print(f'test_speech_recognise: {response}')


async def test_speech_recognise():
    """
    Monitor voice recognition demo
    Listen to speech recognition events, and the robot reports the text after speech recognition
    When the recognized voice is "Wukong", broadcast "Hello, I'm AlphaMini. La-la-la-la-la..."
    Stop listening when the speech is recognized as "end"
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    """
    #  Listening object for voice
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # processors
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        # print("{0}".format(str(msg.text)))
        if str(msg.text) == msg.text:
            # I hear "AlphaMini", tts says hello.
            asyncio.create_task(__tts(msg.text))
            # Listen to the end, stop listening.
            observe.stop()
        elif str(msg.text) == "end":
            # End event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # begin
    observe.start()
    await asyncio.sleep(5)
 

async def test_take_picture():
    """
        test photo
        Let the robot take a picture immediately and wait for the result
        #TakePictureResponse.isSuccess : Was it successful
        #TakePictureResponse.code : return code
        #TakePictureResponse.picPath : The storage path of the photo in the robot
        """
    # response: TakePictureResponse
    # take_picture_type:
    # IMMEDIATELY-take a photo immediately,
    # FINDFACE-find a face and then take a photo, two photo effects
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.FINDFACE).execute()

    print(f'test_take_picture result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_take_picture timetout'
    assert response is not None and isinstance(response,
                                               TakePictureResponse), 'test_take_picture result unavailable'
    assert response.isSuccess, 'test_take_picture failed'


async def test_speech_recognise_controll():
    """
    Monitor voice recognition demo
    Listen to speech recognition events, and the robot reports the text after speech recognition
    If it says take the picture otherwise it says ok, no problem
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    """
    #  Listening object for voice
    observe: ObserveSpeechRecognise = ObserveSpeechRecognise()

    # processors
    # SpeechRecogniseResponse.text
    # SpeechRecogniseResponse.isSuccess
    # SpeechRecogniseResponse.resultCode
    def handler(msg: SpeechRecogniseResponse):
        print(f'=======handle speech recognise:{msg}')
        # print("{0}".format(str(msg.text)))
        if str(msg.text) == 'Yes.':
            asyncio.create_task(test_take_picture())
            # Listen to the end, stop listening.
            observe.stop()
        elif str(msg.text) == 'No.':
            asyncio.create_task(_tts())
            # Listen to the end, stop listening.
            observe.stop()
        else:
            # End event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

    observe.set_handler(handler)
    # begin
    observe.start()
    await asyncio.sleep(5)


async def _tts():
    block: StartPlayTTS = StartPlayTTS(text=f'Ok, no problem')
    response = await block.execute()
    print(f'test_speech_recognise: {response}')


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_play_tts()
    await test_speech_recognise()
    await asyncio.sleep(5)
    await test_speech_recognise_controll()


if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
