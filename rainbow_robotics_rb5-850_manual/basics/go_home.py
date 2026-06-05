# go_home.py
# 로봇을 기존 홈 자세로 복귀시키는 코드 (move_j 기반)
# 프로그램 사용 전후로 실행해 항상 같은 시작/종료 자세를 유지한다.
#
# move_j :: joint = np.array([base, shoulder, elbow, wrist1, wrist2, wrist3])
#           에 입력된 joint 값(단위: degree)으로 이동.
 
import rbpodo as rb
import numpy as np
 
ROBOT_IP = "172.16.3.128"  # 308호 로봇암 주소 (환경에 따라 다름, 사용 전 확인)
 
# 홈 자세 (작업 시작/종료 시 복귀할 기준 자세)
HOME = np.array([91.15, -16, -118.9, 315, -268, 2.39])
 
SPEED = 60   # move_j 속도
ACCEL = 80   # move_j 가속도
 
 
def _main():
    robot = rb.Cobot(ROBOT_IP)
    rc = rb.ResponseCollector()
    try:
        # robot.set_operation_mode(rc, rb.OperationMode.Simulation)
        robot.set_operation_mode(rc, rb.OperationMode.Real)
        rc = rc.error().throw_if_not_empty()
 
        print(f"홈 자세로 복귀: {HOME.tolist()}")
        robot.move_j(rc, HOME, SPEED, ACCEL)
        rc = rc.error().throw_if_not_empty()
 
        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()
 
        print("홈 복귀 완료")
    finally:
        print('Exit')
 
 
if __name__ == '__main__':
    _main()
 
