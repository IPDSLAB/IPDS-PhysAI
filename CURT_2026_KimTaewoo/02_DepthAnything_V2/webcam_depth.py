
import os
import time
import cv2
import torch
import numpy as np
from depth_anything_v2.dpt import DepthAnythingV2

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

model = DepthAnythingV2(
    encoder='vits',
    features=64,
    out_channels=[48, 96, 192, 384]
)

model.load_state_dict(
    torch.load('checkpoints/depth_anything_v2_vits.pth', map_location='cpu')
)
model = model.to(DEVICE).eval()

os.makedirs("captures", exist_ok=True)

cap = cv2.VideoCapture(0)

save_idx = 0
prev_time = time.time()
fps = 0.0

print("DEVICE:", DEVICE)
print("Press s to save RGB/Depth")
print("Press q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("camera read failed")
        break

    depth = model.infer_image(frame, 256)

    depth_norm = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
    depth_gray = (depth_norm * 255).astype(np.uint8)
    depth_color = cv2.applyColorMap(depth_gray, cv2.COLORMAP_INFERNO)

    now = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / (now - prev_time))
    prev_time = now

    cv2.putText(
        depth_color,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2
    )

    view = np.hstack((frame, depth_color))
    cv2.imshow("RGB | Depth Anything V2", view)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        rgb_path = f"captures/rgb_{save_idx:04d}.png"
        depth_path = f"captures/depth_{save_idx:04d}.png"
        depth_raw_path = f"captures/depth_raw_{save_idx:04d}.png"

        cv2.imwrite(rgb_path, frame)
        cv2.imwrite(depth_path, depth_color)
        cv2.imwrite(depth_raw_path, depth_gray)

        print(f"saved: {rgb_path}, {depth_path}, {depth_raw_path}")
        save_idx += 1

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
EOF
