#move_l :: 로봇암 기존 좌표에서 target_point = np.array([x, y, z, rx, ry, rz]) 에 위치 좌표값을 입력된 값만큼 +로 이동.

import rbpodo as rb
import numpy as np


def _main():
    robot = rb.Cobot("172.16.3.128")
    rc = rb.ResponseCollector()

    try:

        #robot.set_operation_mode(rc, rb.OperationMode.Real)
        robot.set_operation_mode(rc, rb.OperationMode.Simulation)
        rc = rc.error().throw_if_not_empty()

        #target_point = np.array([x, y, z, rx, ry, rz])
        target_point = np.array([0, 0, 0, 0, 0, 0])
        robot.move_l_rel(rc, target_point, 300, 400, rb.ReferenceFrame.Base)
        rc = rc.error().throw_if_not_empty()

        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()
    finally:
        print('Exit')


if __name__ == '__main__':
    _main()
