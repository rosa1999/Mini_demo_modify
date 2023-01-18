import asyncio
import logging

from mini import mini_sdk as MiniSdk
from mini.apis.api_action import GetActionList, GetActionListResponse, RobotActionType
from mini.apis.api_action import MoveRobot, MoveRobotDirection, MoveRobotResponse
from mini.apis.api_action import PlayAction, PlayActionResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_get_device_by_name, test_connect, test_start_run_program, shutdown


# Test, execute an action file
async def test_play_action():
    """
    Execute an action demo
    Control the robot to perform a named local (built-in/custom) action and wait for a response
    from the result of the action
    The name of the action can be obtained from the GetActionList.
    #PlayActionResponse.isSuccess : whether it succeeds or not
    #PlayActionResponse.resultCode : Return Code

    """
    # action_name: Action file name, get action supported by robot via GetActionList.
    block: PlayAction = PlayAction(action_name='018')
    # response: PlayActionResponse
    (resultType, response) = await block.execute()

    print(f'test_play_action result:{response}')

'''
    assert resultType == MiniApiResultType.Success, 'test_play_action timetout'
    assert response is not None and isinstance(response, PlayActionResponse), 'test_play_action result unavailable'
    assert response.isSuccess, 'play_action failed'
'''


# Test, control robot, move forward/backward/left/right
async def test_move_robot():
    """
    Control robot move demo
    Control the robot to move 10 steps to the left (LEFTWARD) and wait for the result.
    #MoveRobotResponse.isSuccess : whether it succeeds or not　
    #MoveRobotResponse.code : return code

    """
    # step: move a few steps
    # direction: direction, enumeration type
    block: MoveRobot = MoveRobot(step=11, direction=MoveRobotDirection.LEFTWARD)
    # response : MoveRobotResponse
    (resultType, response) = await block.execute()

    print(f'test_move_robot result:{response}')

'''
    assert resultType == MiniApiResultType.Success, 'test_move_robot timetout'
    assert response is not None and isinstance(response, MoveRobotResponse), 'test_move_robot result unavailable'
    assert response.isSuccess, 'move_robot failed'
'''


# Test, get a list of supported action files
async def test_get_action_list():
    """
    Get action list demo
    Get a list of actions built into the bot and wait for reply results.

    """
    # action_type: INNER is a non-modifiable action file built into the robot,
    # CUSTOM is an action file placed in sdcard/customize/action that can be modified by the developer.
    block: GetActionList = GetActionList(action_type=RobotActionType.INNER)
    # response:GetActionListResponse
    (resultType, response) = await block.execute()

    print(f'test_get_action_list result:{response}')

'''
    assert resultType == MiniApiResultType.Success, 'test_get_action_list timetout'
    assert response is not None and isinstance(response,
                                               GetActionListResponse), 'test_get_action_list result unavailable'
    assert response.isSuccess, 'get_action_list failed'
'''


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_play_action()
    await test_move_robot()
    await test_get_action_list()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
