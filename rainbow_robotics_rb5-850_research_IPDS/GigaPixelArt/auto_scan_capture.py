"""
auto_scan_capture.py
RB5-850 그리드 스캔 촬영 + TCP 포즈 기록 (Canon EOS R8 / gphoto2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
지그재그(snake) 패턴으로 그림 위를 스캔하며 각 지점 촬영
결과: scan_images/ 폴더 (사진 + poses.json)

전제:
  - 시작 전 로봇 TCP가 시작점(X≈170, Z≈350)에 위치해 있어야 함
  - 그림과 렌즈 거리 약 41-42mm 유지 (Y는 고정)
"""

import rbpodo as rb
import gphoto2 as gp
import numpy as np
import asyncio
import os
import json
import time

# ── 설정 ────────────────────────────────────────────────────
ROBOT_IP   = "172.16.3.128"
SAVE_DIR   = "scan_images2"

X_START    = 170.0     # 시작 X (mm) - 참고용 기록
Z_START    = 350.0     # 시작 Z (mm) - 참고용 기록
X_STEP     = 40.0      # X 이동 간격 (mm)
Z_STEP     = 40.0      # Z 이동 간격 (mm)
N_X_MOVES  = 6         # 한 줄당 X 이동 횟수 (→ 줄당 7장)
N_Z_MOVES  = 7         # Z 이동 횟수 (→ 8줄, Z -40 총 7번)

MOVE_SPEED = 100       # mm/s (스캔은 천천히 안정적으로)
MOVE_ACCEL = 200       # mm/s^2
SETTLE_SEC = 0.8       # 이동 후 진동 안정화 대기
SHOOT_SEC  = 1.5       # 촬영 후 대기
# ────────────────────────────────────────────────────────────

os.makedirs(SAVE_DIR, exist_ok=True)

# ── TCP 포즈 읽기용 (async 데이터 채널, 지속 루프) ────────────
_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)
_data_channel = rb.asyncio.CobotData(ROBOT_IP)

def read_tcp_pose():
    """현재 엔드포인트 TCP 포즈 [x,y,z,rx,ry,rz] 읽기"""
    try:
        async def _r():
            d = await _data_channel.request_data()
            return np.array(d.sdata.tcp_ref)   # ← check_tcp_pose.py로 확인한 속성명
        return _loop.run_until_complete(_r())
    except Exception as e:
        print(f"  ⚠️ 포즈 읽기 실패: {e}")
        return None

# ── 이동 시퀀스 생성 (지그재그) ──────────────────────────────
# moves: [('X', +/-40), ..., ('Z', -40), ...]
moves = []
direction = -1                          # 첫 줄: X 감소 방향
for row in range(N_Z_MOVES + 1):        # 총 8줄
    for _ in range(N_X_MOVES):          # 줄당 X 이동 6번
        moves.append(('X', direction * X_STEP))
    if row < N_Z_MOVES:                 # 마지막 줄 뒤에는 Z 이동 없음
        moves.append(('Z', -Z_STEP))
    direction *= -1                     # 다음 줄은 반대 방향

total_shots = 1 + len(moves)            # 시작점 1장 + 이동 후 촬영

# ── 카메라 / 로봇 연결 ───────────────────────────────────────
print("카메라 연결 중...")
camera = gp.Camera()
camera.init()
print("✅ Canon EOS R8 연결됨")

robot = rb.Cobot(ROBOT_IP)
rc = rb.ResponseCollector()
robot.set_operation_mode(rc, rb.OperationMode.Real)
rc = rc.error().throw_if_not_empty()
print("✅ 로봇 연결됨\n")

print("=" * 55)
print("  그리드 스캔 촬영")
print("=" * 55)
print(f"  줄 수: {N_Z_MOVES + 1}  /  줄당 {N_X_MOVES + 1}장")
print(f"  총 촬영: {total_shots}장")
print(f"  X 간격: {X_STEP}mm  /  Z 간격: {Z_STEP}mm")
print("=" * 55)

records = []
cur_x, cur_z = X_START, Z_START
img_index = 0

def capture(idx, cx, cz, note=""):
    """촬영 + 포즈 기록"""
    pose = read_tcp_pose()

    file_path   = camera.capture(gp.GP_CAPTURE_IMAGE)
    camera_file = camera.file_get(
        file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL
    )
    save_path = os.path.join(SAVE_DIR, f"{idx:03d}.jpg")
    camera_file.save(save_path)

    records.append({
        "idx": idx,
        "img": save_path,
        "tcp_pose": pose.tolist() if pose is not None else None,  # 실제 측정 포즈
        "grid_xz": [round(cx, 1), round(cz, 1)],                  # 명령 좌표 (참고)
        "note": note,
    })
    print(f"  [{idx+1}/{total_shots}] 📸 {save_path}  (X={cx:.0f}, Z={cz:.0f}) {note}")

def move_rel(axis, delta):
    """상대 직선 이동 (Base 기준)"""
    rel = np.zeros(6)
    if axis == 'X':
        rel[0] = delta
    elif axis == 'Z':
        rel[2] = delta
    robot.move_l_rel(rc, rel, MOVE_SPEED, MOVE_ACCEL, rb.ReferenceFrame.Base)
    rc.error().throw_if_not_empty()
    if robot.wait_for_move_started(rc, 0.5).is_success():
        robot.wait_for_move_finished(rc)
    rc.error().throw_if_not_empty()
    time.sleep(SETTLE_SEC)

try:
    # 1) 시작점 촬영
    print("\n시작점 촬영...")
    capture(img_index, cur_x, cur_z, note="start")
    img_index += 1
    time.sleep(SHOOT_SEC)

    # 2) 이동하며 촬영
    for axis, delta in moves:
        move_rel(axis, delta)
        if axis == 'X':
            cur_x += delta
        else:
            cur_z += delta
        capture(img_index, cur_x, cur_z, note=f"{axis}{delta:+.0f}")
        img_index += 1
        time.sleep(SHOOT_SEC)

    # 3) 포즈 기록 저장
    with open(os.path.join(SAVE_DIR, "poses.json"), "w") as f:
        json.dump(records, f, indent=2)

    print("\n" + "=" * 55)
    print(f"  ✅ 스캔 완료: {len(records)}장 촬영")
    print(f"  📁 {SAVE_DIR}/poses.json 저장")
    print("=" * 55)

finally:
    camera.exit()
    _loop.close()
    print("종료")
