# move_j :: joint = np.array([base, shoulder, elbow, wrist1, wrist2, wrist3]) 에 입력된 joint 값으로 이동.

import rbpodo as rb
import numpy as np


def _main():
    robot = rb.Cobot("172.16.3.128")
    rc = rb.ResponseCollector()

    try:
        #robot.set_operation_mode(rc, rb.OperationMode.Simulation)
        robot.set_operation_mode(rc, rb.OperationMode.Real)
        rc = rc.error().throw_if_not_empty()

        #joint = np.array([0, 0, 0, 0, 0, 0]) #기존 코드
        joint = np.array([91.15, -16, -118.9, 315, -268, 2.39]) #좌표 설정
        robot.move_j(rc, joint, 60, 80)
        rc = rc.error().throw_if_not_empty()

        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()
    finally:
        print('Exit')


if __name__ == '__main__':
    _main()
