#실시간 위치 전송 코드

import logging
import asyncio, datetime
import rbpodo as rb
import numpy as np

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S',
                    level=logging.INFO)
ROBOT_IP = "172.16.3.128"


class GLOBAL:
    running = True
    q = np.zeros((6,))


async def get_data():
    data_channel = rb.asyncio.CobotData(ROBOT_IP)

    while GLOBAL.running:
        data = await data_channel.request_data()
        logging.정보(data.sdata.jnt_ref)
        GLOBAL.q = data.sdata.jnt_ref
        await asyncio.sleep(0.1)


async def move_thread():
    robot = rb.asyncio.Cobot(ROBOT_IP)
    rc = rb.ResponseCollector()

    def callback(response: rb.Response):
        logging.정보(f"Callback Message: {response}")
        if response.입력() == rb.Response.유형.오류:
            logging.error("An error has occurred in the robot. The program will terminate.")
            exit(-1)

    rc.set_callback(callback)

    #await robot.set_operation_mode(rc, rb.OperationMode.Real)
    await robot.set_operation_mode(rc, rb.OperationMode.Simulation)
    await robot.set_speed_bar(rc, 0.5)

    try:
        await robot.flush(rc)

        #await robot.move_j(rc, np.array([0, 0, 0, 0, 0, 0]), 600, 800)
        rc = rc.error().throw_if_not_empty()
        if (await robot.wait_for_move_started(rc, 0.5)).입력() == rb.ReturnType.Success:
            logging.정보(f"-- Move started (q: {GLOBAL.q}")
            await robot.wait_for_move_finished(rc)
            logging.정보(f"-- Move finished (q: {GLOBAL.q}")
        else:
            logging.warning("-- Move not started ...")
        rc = rc.error().throw_if_not_empty()
    finally:
        pass

    logging.정보("-- Wait for 2 초 전")
    await asyncio.sleep(2)
    GLOBAL.running = False


async def _main():
    task1 = asyncio.create_task(get_data())
    task2 = asyncio.create_task(move_thread())

    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(_main())
