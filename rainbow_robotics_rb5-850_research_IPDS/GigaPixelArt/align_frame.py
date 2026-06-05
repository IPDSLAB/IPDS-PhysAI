"""
align_frame.py
액자 모서리 ↔ 카메라 화면 수평 정렬 도우미 (Canon EOS R8 라이브뷰)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
라이브뷰로 액자 변의 기울기를 실시간 표시
로봇 RZ를 돌려가며 액자 윗변이 화면 가로선과 평행(0°)이 되게 맞춤

화면 표시:
  초록선  = 화면 기준선(완벽한 수평/수직)
  빨강선  = 검출된 액자 변
  숫자    = 액자 변이 기울어진 각도 (0°에 가까울수록 정렬됨)

조작:
  q : 종료
"""

import gphoto2 as gp
import cv2
import numpy as np

# ── 격자 설정 ────────────────────────────────────────────────
GRID_COLS = 6    # 세로선 분할 (열)
GRID_ROWS = 4    # 가로선 분할 (행)  → 4 x 3 = 12칸
# ────────────────────────────────────────────────────────────

def analyze(frame):
    """액자 변 검출 → 기울기 각도 계산 + 오버레이"""
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80,
                            minLineLength=w//4, maxLineGap=20)

    overlay = frame.copy()

    # 화면 기준 격자 (초록) - GRID_COLS x GRID_ROWS 칸
    for c in range(1, GRID_COLS):
        x = w * c // GRID_COLS
        cv2.line(overlay, (x, 0), (x, h), (0, 200, 0), 1)
    for r in range(1, GRID_ROWS):
        y = h * r // GRID_ROWS
        cv2.line(overlay, (0, y), (w, y), (0, 200, 0), 1)
    # 바깥 테두리
    cv2.rectangle(overlay, (0, 0), (w - 1, h - 1), (0, 200, 0), 1)

    h_best = None   # 가장 긴 near-수평 선 (액자 윗변)
    v_best = None   # 가장 긴 near-수직 선 (액자 좌변)
    h_len = v_len = 0

    if lines is not None:
        for ln in lines:
            x1, y1, x2, y2 = ln[0]
            ang = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            # -90 ~ 90 으로 접기
            if ang > 90:  ang -= 180
            if ang < -90: ang += 180
            length = np.hypot(x2 - x1, y2 - y1)

            if abs(ang) < 45:          # near 수평
                if length > h_len:
                    h_len, h_best = length, (x1, y1, x2, y2, ang)
            else:                       # near 수직
                if length > v_len:
                    v_len, v_best = length, (x1, y1, x2, y2, ang)

    results = {}

    if h_best:
        x1, y1, x2, y2, ang = h_best
        cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)
        results["h_tilt"] = ang          # 수평으로부터 기울기 (목표 0)

    if v_best:
        x1, y1, x2, y2, ang = v_best
        cv2.line(overlay, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 수직선의 수직으로부터 기울기 (목표 0)
        v_dev = ang - 90 if ang > 0 else ang + 90
        results["v_tilt"] = v_dev

    return overlay, results


# ── 카메라 연결 ──────────────────────────────────────────────
print("카메라 연결 중...")
camera = gp.Camera()
camera.init()
print("✅ 라이브뷰 시작 (q: 종료)\n")

while True:
    try:
        preview = camera.capture_preview()
        data    = preview.get_data_and_size()
        frame   = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
    except gp.GPhoto2Error as e:
        print(f"라이브뷰 오류: {e}")
        break

    if frame is None:
        continue

    overlay, res = analyze(frame)
    h, w = overlay.shape[:2]

    # 각도 텍스트
    if "h_tilt" in res:
        c = (0, 255, 0) if abs(res["h_tilt"]) < 0.5 else (0, 255, 255)
        msg = f"윗변 기울기: {res['h_tilt']:+.2f}도"
        if abs(res["h_tilt"]) < 0.5: msg += "  OK"
        else: msg += f"  -> RZ {-res['h_tilt']:+.2f}도 회전"
        cv2.putText(overlay, msg, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, c, 2)
    else:
        cv2.putText(overlay, "윗변 미검출 - 액자가 화면에 보이게", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if "v_tilt" in res:
        c = (0, 255, 0) if abs(res["v_tilt"]) < 0.5 else (0, 255, 255)
        cv2.putText(overlay, f"좌변 기울기: {res['v_tilt']:+.2f}도", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, c, 2)

    # 화면 표시 (너무 크면 축소)
    if w > 1280:
        overlay = cv2.resize(overlay, (1280, int(h * 1280 / w)))
    cv2.imshow("Frame Alignment (q: quit)", overlay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.exit()
cv2.destroyAllWindows()
print("종료")
