import asyncio
import logging
import mini.mini_sdk as MiniSdk
from mini.dns.dns_browser import WiFiDevice


from mini.apis.api_behavior import StartBehavior
from mini.apis.api_observe import ObserveHeadRacket, HeadRacketType
from mini.pb2.codemao_observeheadracket_pb2 import ObserveHeadRacketResponse
from test.test_connect import test_connect, shutdown
from test.test_connect import test_get_device_by_name, test_start_run_program


# Test, touch listen.
async def test_ObserveHeadRacket():
    """
    Monitor the head event demo

    Monitor the head event, when the head of the robot is tapped, report the head type

    When the robot's head is double-clicked, stop listening and do a dance

    # ObserveHeadRacketResponse.type:

    # class HeadRacketType(enum.Enum):

    # SINGLE_CLICK = 1 # click

    # LONG_PRESS = 2 # Long press

    # DOUBLE_CLICK = 3 # double click

    """

    # Create a listen
    observer: ObserveHeadRacket = ObserveHeadRacket()
    # Event processors
    # ObserveHeadRacketResponse.type:
    # @enum.unique
    # class HeadRacketType(enum.Enum):
    # SINGLE_CLICK = 1 # Click on the
    # LONG_PRESS = 2 # Press and hold...
    # DOUBLE_CLICK = 3 # DOUBLE_CLICK

    def handler(msg: ObserveHeadRacketResponse):
        # Stop listening when an event is monitored,
        print("{0}".format(str(msg.type)))
        # if msg.type == HeadRacketType.DOUBLE_CLICK.value:
        observer.stop()
        # Execute a dance
        asyncio.create_task(__dance())

    observer.set_handler(handler)
    # begin
    observer.start()
    await asyncio.sleep(0)


async def __dance():
    await ControlBehavior(name="dance_0002").execute()
    await StartBehavior(name="dance_0002").execute()
    # end event_loop
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_ObserveHeadRacket()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
