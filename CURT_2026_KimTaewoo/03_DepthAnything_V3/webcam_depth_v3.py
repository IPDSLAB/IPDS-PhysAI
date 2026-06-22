import os
import time
import cv2
import torch
import numpy as np

from depth_anything_3.api import DepthAnything3

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_DIR = "depth-anything/DA3NESTED-GIANT-LARGE-1.1"

CAM_ID = 0
WIDTH = 320
HEIGHT = 240
PROCESS_RES = 128

INFER_EVERY = 1   # 10프레임마다 V3 추론. 낮추면 더 자주 추론하지만 느려짐.

SAVE_DIR = "captures_v3"
os.makedirs(SAVE_DIR, exist_ok=True)

print("Loading Depth Anything V3 model...")
model = DepthAnything3.from_pretrained(MODEL_DIR)
model = model.to(device=DEVICE)
model.eval()

print("DEVICE:", DEVICE)
print("Press s to save RGB/Depth/NPZ")
print("Press q to quit")

cap = cv2.VideoCapture(CAM_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

last_depth_color = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
last_depth_raw = None
last_conf = None
last_intrinsics = None
last_extrinsics = None

save_idx = 0
frame_idx = 0

prev_time = time.time()
fps = 0.0
last_infer_time = 0.0

while True:
    ret, frame = cap.read()

    if not ret:
        print("camera read failed")
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    now = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev_time, 1e-6))
    prev_time = now

    if frame_idx % INFER_EVERY == 0:
        try:
            t0 = time.time()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            prediction = model.inference(
                [rgb],
                process_res=PROCESS_RES,
            )

            depth = prediction.depth[0]
            conf = prediction.conf[0]
            intrinsics = prediction.intrinsics[0]
            extrinsics = prediction.extrinsics[0]

            depth_norm = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
            depth_gray = (depth_norm * 255).astype(np.uint8)
            depth_gray = cv2.resize(depth_gray, (WIDTH, HEIGHT))
            depth_color = cv2.applyColorMap(depth_gray, cv2.COLORMAP_INFERNO)

            last_depth_color = depth_color
            last_depth_raw = depth
            last_conf = conf
            last_intrinsics = intrinsics
            last_extrinsics = extrinsics

            last_infer_time = time.time() - t0

        except Exception as e:
            print("V3 inference error:", repr(e))

    display_depth = last_depth_color.copy()

    cv2.putText(
        display_depth,
        f"FPS: {fps:.1f}",
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        display_depth,
        f"V3 infer: {last_infer_time:.2f}s",
        (15, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    view = np.hstack((frame, display_depth))
    cv2.imshow("RGB | Depth Anything V3", view)

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
