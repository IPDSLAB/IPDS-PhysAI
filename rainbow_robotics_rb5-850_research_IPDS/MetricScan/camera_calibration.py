"""
[STEP 1] 카메라 캘리브레이션 - Canon EOS R8 (gphoto2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
체커보드를 다양한 각도/위치에서 15~20장 촬영
결과: camera_params.npz

조작:
  엔터      → 촬영
  y         → 이 사진 사용
  n         → 다시 촬영
  c + 엔터  → 캘리브레이션 계산 (10장 이상일 때)
  q + 엔터  → 종료

  SQUARE_SIZE = 30.0   # ← 여기를 실제 측정값으로 수정
"""

import gphoto2 as gp
import cv2
import numpy as np
import os

# ── 설정 ────────────────────────────────────────────────────
CHECKERBOARD = (9, 6)    # 내부 코너 수 - checkerboard_print.py로 만든 것 기준
SQUARE_SIZE  = 30.0      # !! 출력 후 자로 측정한 실제 칸 크기 (mm) 입력 !!
SAVE_DIR     = "calib_images"
# ────────────────────────────────────────────────────────────

os.makedirs(SAVE_DIR, exist_ok=True)

# 체커보드 3D 실세계 좌표
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

obj_points = []
img_points = []
count = 0

# 카메라 초기화
print("카메라 연결 중...")
camera = gp.Camera()
camera.init()
print("✅ Canon EOS R8 연결됨\n")

print("=" * 50)
print("  카메라 캘리브레이션")
print("=" * 50)
print(f"  체커보드: {CHECKERBOARD[0]}x{CHECKERBOARD[1]} 내부 코너")
print(f"  칸 크기: {SQUARE_SIZE}mm")
print(f"  목표: 15~20장")
print("=" * 50)
print("\n  체커보드를 다양한 각도로 기울여가며 촬영하세요")
print("  (정면, 좌우 기울기, 상하 기울기, 코너 쪽 등)")
print()

def capture_and_check():
    """촬영 후 체커보드 감지 확인"""
    print("  📷 촬영 중...")

    # gphoto2 촬영 (참고 코드 패턴)
    file_path   = camera.capture(gp.GP_CAPTURE_IMAGE)
    camera_file = camera.file_get(
        file_path.folder,
        file_path.name,
        gp.GP_FILE_TYPE_NORMAL
    )
    file_data  = camera_file.get_data_and_size()
    image_data = np.frombuffer(file_data, dtype=np.uint8)
    frame      = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    if frame is None:
        print("  ❌ 이미지 디코딩 실패")
        return None, None, False

    # 체커보드 감지
    gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flags  = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK
    found, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, flags)

    # 결과 미리보기 (1/4 축소)
    preview = cv2.resize(frame, (frame.shape[1]//4, frame.shape[0]//4))

    if found:
        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1),
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )
        # 미리보기에 코너 표시
        corners_small = corners2 / 4
        cv2.drawChessboardCorners(preview, CHECKERBOARD, corners_small, found)
        cv2.putText(preview, "OK - y:저장  n:다시", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        print("  ✅ 체커보드 감지됨")
    else:
        cv2.putText(preview, "FAIL - 미감지  n:다시", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        print("  ❌ 체커보드 미감지")
        corners2 = None

    cv2.imshow("Step1 - Calibration", preview)
    cv2.waitKey(1)

    return frame, corners2, found


while True:
    cmd = input(f"[{count}장 저장됨] 엔터:촬영 / c:캘리브레이션 / q:종료 → ").strip().lower()

    if cmd == 'q':
        break

    elif cmd == 'c':
        if count < 10:
            print(f"  ⚠️  최소 10장 필요 (현재 {count}장)")
            continue

        print(f"\n  ⏳ {count}장으로 캘리브레이션 계산 중...")
        img_size = cv2.imread(f"{SAVE_DIR}/calib_001.jpg").shape[1::-1]
        rms, K, dist, _, _ = cv2.calibrateCamera(
            obj_points, img_points, img_size, None, None
        )
        print("\n" + "=" * 50)
        print(f"  ✅ 완료!  재투영 오차: {rms:.4f} px  (0.5 이하 권장)")
        print(f"  fx={K[0,0]:.1f}  fy={K[1,1]:.1f}")
        print(f"  cx={K[0,2]:.1f}  cy={K[1,2]:.1f}")
        print("=" * 50)
        np.savez("camera_params.npz", K=K, dist=dist, rms=rms)
        print("  📁 camera_params.npz 저장 → step2 진행 가능")
        break

    else:
        # 촬영
        frame, corners2, found = capture_and_check()

        if frame is None:
            continue

        if not found:
            print("  → 체커보드가 잘 보이도록 위치 조정 후 다시 촬영하세요\n")
            continue

        keep = input("  저장할까요? y/n → ").strip().lower()
        if keep == 'y':
            count += 1
            save_path = f"{SAVE_DIR}/calib_{count:03d}.jpg"
            cv2.imwrite(save_path, frame)
            obj_points.append(objp)
            img_points.append(corners2)
            print(f"  💾 저장: {save_path}  ({count}장)\n")
        else:
            print("  → 다시 촬영하세요\n")

camera.exit()
cv2.destroyAllWindows()
print("종료")
