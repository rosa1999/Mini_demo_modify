import asyncio
import logging

from mini import mini_sdk as MiniSdk

from mini.apis import errors
from mini.apis.api_behavior import StartBehavior, ControlBehaviorResponse, StopBehavior
from mini.apis.api_expression import ControlMouthLamp, ControlMouthResponse
from mini.apis.api_expression import PlayExpression, PlayExpressionResponse
from mini.apis.api_expression import SetMouthLamp, SetMouthLampResponse, MouthLampColor, MouthLampMode
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# Test the eyes to make a face
async def test_play_expression():
    """

    Test play expressions
    Let the bot play a built-in emoticon called "codemao1" and wait for the reply results!
    #PlayExpressionResponse.isSuccess : Success or not
    #PlayExpressionResponse.resultCode : Return Code

    """

    block: PlayExpression = PlayExpression(express_name="codemao1")
    # response: PlayExpressionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_expression result: {response}')

'''
assert resultType == MiniApiResultType.Success, 'test_play_expression timetout'
      assert response is not None and isinstance(response,
                                                 PlayExpressionResponse), 'test_play_expression result unavailable'
      assert response.isSuccess, 'play_expression failed'
'''


# Test, make the robot dance/stop dancing
async def test_control_behavior():
    """
    test control expressivity
    Ask the robot to start a dance called "dance_0004" and wait for the response.

    """
    # control_type: START, STOP
    block: StartBehavior = StartBehavior(name="dance_0004en")
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()

    print(f'test_control_behavior result: {response}')
    print(
        'resultCode = {0}, error = {1}'.format(response.resultCode, errors.get_express_error_str(response.resultCode)))

'''
    assert resultType == MiniApiResultType.Success, 'test_control_behavior timetout'
    assert response is not None and isinstance(response,
                                               ControlBehaviorResponse), 'test_control_behavior result unavailable'
    assert response.isSuccess, 'control_behavior failed'
'''

"""
async def test_stop_behavior():
    # start
    block: StartBehavior = StartBehavior(name="dance_0004en")
    # response ControlBehaviorResponse
    (resultType, response) = await block.execute()
    print(f'test_stop_behavior result: {response}')

    # asyncio.create_task(await block.execute())

    # stop after 5 seconds
    await asyncio.sleep(5)
    block: StopBehavior = StopBehavior()
    (resultType, response) = await block.execute()
    print(f' test_stop_behavior result: {response} ')
"""


# Test, set the mouth light to green Always on
async def test_set_mouth_lamp():
    # mode: mouthlamp mode, 0: normal mode, 1: breath mode
    # color: mouth light color, 1: red, 2: green
    # duration: duration in milliseconds, -1 means always on.
    # breath_duration: duration of a blink in milliseconds

    """
    Test Set Mouth Light
    Set the robot's mouth light to normal mode, green and always on for 3s, and wait for the reply result.
    When mode=NORMAL, the duration parameter works, indicating how long it will be always on.
    When mode=BREATH, the breath_duration parameter works, indicating how often to breathe
    #SetMouthLampResponse.isSuccess : Success or Not
    #SetMouthLampResponse.resultCode : return code

    """

    block: SetMouthLamp = SetMouthLamp(color=MouthLampColor.GREEN, mode=MouthLampMode.NORMAL,
                                       duration=3000, breath_duration=1000)
    # response:SetMouthLampResponse
    (resultType, response) = await block.execute()

    print(f'test_set_mouth_lamp result: {response}')

    '''
    assert resultType == MiniApiResultType.Success, 'test_set_mouth_lamp timetout'
    assert response is not None and isinstance(response, SetMouthLampResponse), 'test_set_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'set_mouth_lamp failed'
    '''


# Test, switch mouth light
async def test_control_mouth_lamp():
    """
    test_control_mouth_lamp
    Have the robot turn off its mouth light and wait for the results.
    #ControlMouthResponse.isSuccess : whether it succeeds or not
    #ControlMouthResponse.resultCode : return code

    """
    # is_open: True,False
    # response :ControlMouthResponse
    (resultType, response) = await ControlMouthLamp(is_open=False).execute()

    print(f'test_control_mouth_lamp result: {response}')

    '''
    assert resultType == MiniApiResultType.Success, 'test_control_mouth_lamp timetout'
    assert response is not None and isinstance(response,
                                               ControlMouthResponse), 'test_control_mouth_lamp result unavailable'
    assert response.isSuccess or response.resultCode == 504, 'control_mouth_lamp failed'
'''


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_play_expression()
    await test_control_behavior()
    await test_set_mouth_lamp()
    await test_control_mouth_lamp()




if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())

