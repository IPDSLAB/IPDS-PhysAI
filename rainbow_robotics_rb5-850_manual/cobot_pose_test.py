from rb_pose_head import *  # 로봇 제어에 필요한 기능들이 들어있는 파일 불러오기

vel = 20  # 로봇의 속도 설정
acc = 100  # 로봇의 가속도 설정
pendant_speed = 0.2  # 로봇 리모컨(펜던트)의 속도 (0~1 사이 값)

RB5_Home()  # 로봇을 처음 위치로 이동시킴

# 목표 위치들 미리 저장해두기
pose1 = [80.03, -820, 116, 179, 0, 180]
pose2 = [80.03, -852.5, 107.64, -178.63, 0, 180]
pose3 = [66.35, -861.92, 325.57, -179.19, 0, 180]
pose4 = [59.03, -896.24, 251, 160, 0, 180]
pose5 = [57, -893, 215, 131, 0, 180]

idx = 1  # 몇 번째 위치로 갈지 정하는 숫자
total_pose_num = 5  # 전체 위치 수 
SetPendantSpeed(pendant_speed)  # 리모컨 속도 설정

try:
    while True:  # 무한 반복 (계속 움직이게 함)
        print(cobot.GetCurrentTCP())  # 현재 로봇 위치를 화면에 출력

        # 현재 위치 순서(idx)에 따라 각각의 위치로 이동
        if (idx % total_pose_num == 0):
            MoveL_arr(pose1)
        elif (idx % total_pose_num == 1):
            MoveL_arr(pose2)
        elif (idx % total_pose_num == 2):
            MoveL_arr(pose3)
        elif (idx % total_pose_num == 3):
            MoveL_arr(pose4)
        elif (idx % total_pose_num == 4):
            MoveL_arr(pose5)

        idx += 1  # 다음 위치로 가기 위해 숫자 증가
        time.sleep(0.5)  # 잠깐 쉬기 (0.5초)

except KeyboardInterrupt:  # 키보드에서 Ctrl+C 누르면 아래 코드 실행
    print("프로그램 종료")  # 프로그램 종료 메시지 출력
    cobot.MotionHalt()  # 로봇 움직임 멈춤
    cobot.DisConnectToCB()  # 로봇 연결 해제

# 이 코드는 로봇이 5개의 위치를 계속 반복해서 움직이도록 만들고,
# 사용자가 멈추기 전까지 자동으로 돌아다님
