import time  # 시간 관련 기능 사용
from rainbow import cobot  # 로봇을 제어하는 cobot 라이브러리 불러오기

# === 로봇 초기 연결 및 설정 ===
cobot.ToCB('172.16.3.128')  # 로봇의 IP 주소를 통해 연결하기
print("debug")  # 디버그용 출력
cobot.CobotInit()  # 로봇 초기화 
cobot.SetProgramMode(cobot.PG_MODE.REAL)  # 실제 모드로 설정 (진짜로 로봇이 움직임)
time.sleep(2)  # 2초 동안 잠시 대기
print("Complete Initialization...")  # 초기화 완료 메시지 출력

# === 속도 설정 ===
vel = 100  # 로봇의 이동 속도
acc = 100  # 로봇의 가속도
pendant_speed = 1  # 리모컨 속도 (1이면 가장 빠름)

# === 펜던트(리모컨) 속도 설정 함수 ===
def SetPendantSpeed(speed):
    # 리모컨으로 조작할 때의 속도를 바꿔주는 함수
    cobot.SetBaseSpeed(speed)

# === 홈 위치로 이동하는 함수 ===
def RB5_Home():
    # 홈 위치: 로봇이 출발할 기본 위치
    SetPendantSpeed(pendant_speed)  # 리모컨 속도 설정
    cobot.MoveL([110.11, -670.64, 448.15, 179.78, 0.06, 180], vel, acc)  # 직선 이동
    time.sleep(0.5)  # 잠깐 대기
    while not cobot.IsIdle():  # 로봇이 멈출 때까지 계속 확인
        print("running")  # 아직 움직이는 중이면 출력
    print("Ready")  # 다 움직이고 나면 출력

# === 원하는 위치로 이동하는 함수 ===
def MoveL_arr(coord):
    # coord는 [x, y, z, rx, ry, rz] 좌표 형식
    x, y, z, ax, ay, az = coord  # 좌표를 각 변수로 분리
    cobot.MoveL([x, y, z, ax, ay, az], vel, acc)  # 해당 위치로 직선 이동
    time.sleep(0.5)  # 이동 후 잠깐 쉬기
    while not cobot.IsIdle():  # 로봇이 멈출 때까지 기다림
        pass
    print("Position moved successfully.")  # 이동 완료 메시지
