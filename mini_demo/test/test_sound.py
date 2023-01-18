import asyncio
import logging

import mini.mini_sdk as MiniSdk

from mini.apis import *
from mini.apis import errors
from mini.apis.api_sound import ChangeRobotVolume, ChangeRobotVolumeResponse
from mini.apis.api_sound import FetchAudioList, GetAudioListResponse, AudioSearchType
from mini.apis.api_sound import PlayAudio, PlayAudioResponse, AudioStorageType
# from mini.apis.api_sound import PlayOnlineMusic, MusicResponse
from mini.apis.api_sound import StartPlayTTS, StopPlayTTS, ControlTTSResponse
from mini.apis.api_sound import StopAllAudio, StopAudioResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, test_start_run_program, shutdown
from test.test_connect import test_get_device_by_name


# Testing text synthesized sounds
async def test_play_tts():
    """
    test_play_tts
    Make the robot start playing a tts saying "Hello, I'm AlphaMini, la-la-la-la" and wait for the result.
    #ControlTTSResponse.isSuccess : if successful
    #ControlTTSResponse.resultCode : return code
    """
    # is_serial:serial execution
    # text: the text to combine
    block: StartPlayTTS = StartPlayTTS(text="Hello, I'm AlphaMini, la-la-la")
    # Returns a tuple, response is a ControlTTSResponse
    (resultType, response) = await block.execute()

    print(f'test_play_tts result: {response}')
    # StartPlayTTS block response contains resultCode and isSuccess
    # If resultCode ! =0 can be queried by errors.get_speech_error_str(response.resultCode))
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

'''
    assert resultType == MiniApiResultType.Success, 'test_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_play_tts result unavailable'
    assert response.isSuccess, 'test_play_tts failed'
'''

'''
async def test_stop_play_tts():
    """
    Test stop playing tts

    Make the robot start to play a long text TTS, the content is 
    Hello, I am Goku, la la la la la la la la chea la la la la la la la cheay la la la la la , don't wait result
    After 2s, make the robot stop playing tts

    #ControlTTSResponse.isSuccess : Is it successful

    #ControlTTSResponse.resultCode : return code

    """
    # is_serial:serial execution
    # text:the text to synthesize
    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="Hello, I'm Goku, blah blah blah blah blah blah blah blah \
    blah blah blah blah blah blah blah blah blah blah")
    # Return bool to indicate whether the sending is successful
    await block.execute()

    await asyncio.sleep(2)

    (resultType, response) = await StopPlayTTS().execute()

    print(f'test_stop_play_tts result: {response}')
    # StopPlayTTS block的response包含resultCode和isSuccess
    # if resultCode !=0 able to pass errors.get_speech_error_str(response.resultCode)) 
    # Query error description information
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_stop_play_tts timetout'
    assert response is not None and isinstance(response, ControlTTSResponse), 'test_stop_play_tts result unavailable'
    assert response.isSuccess, 'test_stop_play_tts failed'
'''


# Test playing sound effects (online)
async def test_play_online_audio():
    """
    test_play_online_audio
    Make the robot play an online sound effect, e.g.:
    "http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3"
    Supported formats are mp3, amr, wav, etc.
    And wait for the results.
    #PlayAudioResponse.isSuccess : whether it succeeds or not
    #PlayAudioResponse.resultCode : return code

    """
    # Play sound effects, url is the list of sound effects to play.
    block: PlayAudio = PlayAudio(
        url="http://hao.haolingsheng.com/ring/000/995/52513bb6a4546b8822c89034afb8bacb.mp3",
        storage_type=AudioStorageType.NET_PUBLIC)
    # response is a PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f'test_play_online_audio result: {response}')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

"""
    assert resultType == MiniApiResultType.Success, 'test_play_online_audio timetout'
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_online_audio result unavailable'
    assert response.isSuccess, 'test_play_online_audio failed'
"""


async def test_play_local_audio():
    """
    Test playing local sound effects

    Make the robot play a local built-in sound effect, the sound effect name is "read_016", and wait for the result

    #PlayAudioResponse.isSuccess : Is it successful

    #PlayAudioResponse.resultCode : return code

    """

    block: PlayAudio = PlayAudio(
        url="read_016",
        storage_type=AudioStorageType.PRESET_LOCAL)
    # response is PlayAudioResponse
    (resultType, response) = await block.execute()

    print(f' test_play_local_audio result: {response} ')
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, ' test_play_local_audio timetout '
    assert response is not None and isinstance(response, PlayAudioResponse), 'test_play_local_audio result unavailable'
    assert response.isSuccess, 'test_play_local_audio failed'


# Test the sound resources of the acquisition robot
async def test_get_audio_list():
    """
    Test to play local sound effects
    Make the bot play a locally built-in sound effect named "read_016" and wait for the result.
    #PlayAudioResponse.isSuccess : whether it succeeds or not
    #PlayAudioResponse.resultCode : return code

    """
    # search_type:
    # AudioSearchType.INNER Refers to the non-modifiable sound effects built into the robot,
    # AudioSearchType.CUSTOM It is placed in the sdcard/customize/music directory and can not be modified by developers
    ''' block: FetchAudioList = FetchAudioList(search_type=AudioSearchType.INNER)
    # response is GetAudioListResponse
    (resultType, response) = await block.execute()

    print(f' test_get_audio_list result: {response} ')

    assert resultType == MiniApiResultType.Success, 'test_get_audio_list timetout'
    assert response is not None and isinstance(response, GetAudioListResponse), 'test_play_audio result unavailable'
    assert response.isSuccess, 'test_get_audio_list failed'
'''

block: PlayAudio = PlayAudio(url="read_016", storage_type=AudioStorageType.PRESET_LOCAL)
# response is a PlayAudioResponse
(resultType, response) = asyncio.run(block.execute())

print(f'test_play_local_audio result: {response}')
assert resultType is not None,\
    print('resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_speech_error_str(response.resultCode)))

'''
# Test stop playing tts
async def test_stop_audio_tts():
    """
    Test stop all audio that is playing

    Play a period of tts first, after 3s, stop all sound effects, and wait for the result

    #StopAudioResponse.isSuccess : Is it successful?

    #StopAudioResponse.resultCode : return code

    """
    # Set is_serial=False, which means that you only need to send the command to the robot, 
    # and await does not need to wait for the robot to execute the result before returning
    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="You let me talk, let me talk, don't interrupt me, "
                                                             "don't interrupt me, don't interrupt me")
    response = await block.execute()
    print(f' test_stop_audio.play_tts: {response} ')
    await asyncio.sleep(3)

    # stop all sounds
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f' test_stop_audio:{response}')

    block: StartPlayTTS = StartPlayTTS(text="Second time, you make me say, let me say, don't interrupt me, "
                                            "don't interrupt me, don't interrupt me")
    asyncio.create_task(block.execute())
    print(f' test_stop_audio.play_tts: {response} ')
    await asyncio.sleep(3)


    assert resultType == MiniApiResultType.Success, 'test_stop_audio timetout'
    assert response is not None and isinstance(response, StopAudioResponse), 'test_stop_audio result unavailable'
    assert response.isSuccess, 'test_stop_audio failed'

# To test, change the volume of the robot
async def test_change_robot_volume():
    """
    Adjust robot volume demo

    Set the volume of the robot to 0.5 and wait for the reply result

    #ChangeRobotVolumeResponse.isSuccess : Is it successful

    #ChangeRobotVolumeResponse.resultCode : return code
    """
    
    # volume: 0~1.0
    block: ChangeRobotVolume = ChangeRobotVolume(volume=0.5)
    # response:ChangeRobotVolumeResponse
    (resultType, response) = await block.execute()

    print(f' test_change_robot_volume result:{response} ')

    assert resultType == MiniApiResultType.Success, 'test_change_robot_volume timetout'
    assert response is not None and isinstance(response,
                                               ChangeRobotVolumeResponse), 'test_change_robot_volume result unavailable'
    assert response.isSuccess, 'get_action_list failed'
'''


async def test_stop_audio():
    """
    The test stops all audio that is playing
    First play a tts, after 3s, stop all sound effects and wait for the result
    #StopAudioResponse.isSuccess : whether or not it succeeds　
    #StopAudioResponse.resultCode : return code

    """
    #  Set is_serial=False, which means you just send the command to the robot, and the wait doesn't need to wait for
    #  the robot to return the result.
    block: StartPlayTTS = StartPlayTTS(is_serial=False, text="You let me talk, let me talk, don't interrupt me, "
                                                             "don't interrupt me, don't interrupt me.")
    response = await block.execute()
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)

    # Stop all sound
    block: StopAllAudio = StopAllAudio()
    (resultType, response) = await block.execute()

    print(f'test_stop_audio:{response}')

    block: StartPlayTTS = StartPlayTTS(text="For the second time, you let me talk, let me talk, don't interrupt me, "
                                            "don't interrupt me, don't interrupt me.")
    asyncio.create_task(block.execute())
    print(f'test_stop_audio.play_tts: {response}')
    await asyncio.sleep(3)


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_play_tts()
    await test_play_online_audio()
    await test_get_audio_list()
    await test_stop_audio()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
