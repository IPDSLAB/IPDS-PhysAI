import os
import time
import cv2
import torch
import numpy as np

from depth_anything_3.api import DepthAnything3

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_DIR = "depth-anything/DA3-SMALL"

CAM_ID = 0

# 화질 개선
WIDTH = 640
HEIGHT = 480
PROCESS_RES = 512

# 느리면 5, 더 부드럽게 보려면 3
INFER_EVERY = 0.5

# 화면 표시 크기
DISPLAY_SCALE = 1.0

SAVE_DIR = "captures_v3"
os.makedirs(SAVE_DIR, exist_ok=True)

def colorize_depth(depth):
    depth = np.asarray(depth, dtype=np.float32)
    depth = np.nan_to_num(depth)

    # 너무 튀는 값 제거
    d_min = np.percentile(depth, 2)
    d_max = np.percentile(depth, 98)

    depth = np.clip(depth, d_min, d_max)
    depth_norm = ((depth - d_min) / (d_max - d_min + 1e-6) * 255).astype(np.uint8)

    # 패치 노이즈 완화
    depth_norm = cv2.bilateralFilter(depth_norm, 9, 75, 75)

    # 경계가 잘 보이는 컬러맵
    depth_color = cv2.applyColorMap(depth_norm, cv2.COLORMAP_TURBO)

    return depth_color

print("Loading Depth Anything V3 model...")
model = DepthAnything3.from_pretrained(MODEL_DIR)
model = model.to(device=DEVICE)
model.eval()

print("DEVICE:", DEVICE)
print("MODEL:", MODEL_DIR)
print("WIDTH x HEIGHT:", WIDTH, HEIGHT)
print("PROCESS_RES:", PROCESS_RES)
print("Press s to save RGB/Depth/NPZ")
print("Press q to quit")

cap = cv2.VideoCapture(CAM_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

last_depth_color = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
last_depth_raw = None
last_conf = None
last_intrinsics = None
last_extrinsics = None

save_idx = 0
frame_idx = 0

prev_time = time.time()
camera_fps = 0.0
infer_fps = 0.0
last_infer_time = 0.0

while True:
    ret, frame = cap.read()

    if not ret:
        print("camera read failed")
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    now = time.time()
    camera_fps = 0.9 * camera_fps + 0.1 * (1.0 / max(now - prev_time, 1e-6))
    prev_time = now

    if frame_idx % INFER_EVERY == 0:
        try:
            t0 = time.time()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            with torch.no_grad():
                prediction = model.inference(
                    [rgb],
                    process_res=PROCESS_RES,
                    process_res_method="upper_bound_resize",
                    infer_gs=False,
                    export_dir=None,
                )

            if DEVICE == "cuda":
                torch.cuda.synchronize()

            depth = prediction.depth[0]

            conf = prediction.conf[0] if hasattr(prediction, "conf") else None
            intrinsics = prediction.intrinsics[0] if hasattr(prediction, "intrinsics") else None
            extrinsics = prediction.extrinsics[0] if hasattr(prediction, "extrinsics") else None

            depth_color = colorize_depth(depth)
            depth_color = cv2.resize(depth_color, (WIDTH, HEIGHT))

            last_depth_color = depth_color
            last_depth_raw = depth
            last_conf = conf
            last_intrinsics = intrinsics
            last_extrinsics = extrinsics

            last_infer_time = time.time() - t0
            infer_fps = 1.0 / max(last_infer_time, 1e-6)

        except Exception as e:
            print("V3 inference error:", repr(e))

    display_depth = last_depth_color.copy()

    cv2.putText(display_depth, f"Camera FPS: {camera_fps:.1f}", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(display_depth, f"Infer FPS: {infer_fps:.1f}", (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(display_depth, f"res={PROCESS_RES}, every={INFER_EVERY}", (15, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    view = np.hstack((frame, display_depth))

    if DISPLAY_SCALE != 1.0:
        view = cv2.resize(
            view,
            None,
            fx=DISPLAY_SCALE,
            fy=DISPLAY_SCALE,
            interpolation=cv2.INTER_LINEAR,
        )

    cv2.imshow("RGB | Depth Anything V3 High Quality", view)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        rgb_path = f"{SAVE_DIR}/rgb_{save_idx:04d}.png"
        depth_path = f"{SAVE_DIR}/depth_{save_idx:04d}.png"
        npz_path = f"{SAVE_DIR}/result_{save_idx:04d}.npz"

        cv2.imwrite(rgb_path, frame)
        cv2.imwrite(depth_path, last_depth_color)

        if last_depth_raw is not None:
            np.savez_compressed(
                npz_path,
                image=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                depth=last_depth_raw,
                conf=last_conf,
                intrinsics=last_intrinsics,
                extrinsics=last_extrinsics,
            )
            print(f"saved: {rgb_path}, {depth_path}, {npz_path}")
        else:
            print(f"saved: {rgb_path}, {depth_path} / npz skipped: no V3 depth yet")

        save_idx += 1

    if key == ord("q"):
        break

    frame_idx += 1

cap.release()
cv2.destroyAllWindows()
