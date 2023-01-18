import asyncio
import logging

import mini.mini_sdk as MiniSdk
from mini.apis.api_observe import ObserveSpeechRecognise
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_speechrecognise_pb2 import SpeechRecogniseResponse
import test_connect


async def __tts():
    block: StartPlayTTS = StartPlayTTS(text="Hello, I'm AlphaMini. La-la-la-la-la...")
    response = await block.execute()
    print(f'test_play_tts: {response}')


# Test listening for voice recognition
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
        print("{0}".format(str(msg.text)))
        if str(msg.text) == "AlphaMini":
            # I hear "AlphaMini", tts says hello.
            asyncio.create_task(__tts())
        elif str(msg.text) == "end":
            # Listen to the end, stop listening.
            observe.stop()
            # End event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)

        # if str(msg.text)[-1].isalpha() is False:
        #     if str(msg.text)[:-1].lower() == "Hello":
        #         asyncio.create_task(__tts())

        """
        if str(msg.text).lower() == "Wukong":
            # Listen to "Wukong", tts say hi
            asyncio.create_task(__tts())

        elif str(msg.text).lower() == "Finish":
            # Listen to the end, stop listening
            observe.stop()
            # Finish event_loop
            asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)
        """

    observe.set_handler(handler)
    # begin
    observe.start()
    await asyncio.sleep(0)


async def main():

    await test_connect.test_get_device_by_name()
    client: WiFiDevice = await test_connect.test_get_device_by_name()
    print("Client: ", client)
    await test_connect.test_connect(client)

    await test_speech_recognise()
    await __tts()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
