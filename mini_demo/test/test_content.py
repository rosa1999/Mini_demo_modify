import asyncio
import logging

from mini import mini_sdk as MiniSdk
from mini.apis.api_content import LanType
from mini.apis.api_content import QueryWiKi, WikiResponse
from mini.apis.api_content import StartTranslate, TranslateResponse
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_get_device_by_name, test_connect, test_start_run_program, shutdown


# interrogazione di prova wiki
async def test_query_wiki():
    """
    Query encyclopedia demo

    Query Encyclopedia, query content "You must choose", and wait for the result,
    the robot will broadcast the query result

    #WikiResponse.isSuccess : Is it successful

    #WikiResponse.resultCode : return code

    """
    # query: query keywords
    block: QueryWiKi = QueryWiKi(query='Ubtech')
    # response : WikiResponse
    (resultType, response) = await block.execute()

    print(f'test_query_wiki result: {response}')

    '''
    assert resultType == MiniApiResultType.Success, 'test_query_wiki timetout'
    assert response is not None and isinstance(response, WikiResponse), 'test_query_wiki result unavailable'
    assert response.isSuccess, 'query_wiki failed'
    '''


# Test translation interface
async def test_start_translate():
    """
    Translate demo
    Use Baidu translation to translate "Jacky Cheung" from Chinese to English,
    and wait for the result to be announced by the robot.
    #TranslateResponse.isSuccess : Success or not
    #TranslateResponse.resultCode : Return Code
    # query: keyword
    # from_lan: source language
    # to_lan: target language
    # platform: GOOGLE

    """

    block: StartTranslate = StartTranslate(query="Jacky Cheung", from_lan=LanType.CN, to_lan=LanType.EN)
    # response: TranslateResponse
    (resultType, response) = await block.execute()

    print(f'test_start_translate result: {response}')

    '''
    assert resultType == MiniApiResultType.Success, 'test_start_translate timetout'
    assert response is not None and isinstance(response, TranslateResponse), 'test_start_translate result unavailable'
    assert response.isSuccess, 'start_translate failed'
'''


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_query_wiki()
    await test_start_translate()
    await shutdown()


if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
