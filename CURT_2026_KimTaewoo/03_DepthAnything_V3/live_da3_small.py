import sys, time
sys.path.insert(0, "src")

import cv2
import torch
import numpy as np
from depth_anything_3.api import DepthAnything3

PROCESS_RES = 512
CAM_ID = 0
MODEL_NAME = "da3mono-large"   # try: da3-small / da3-base / da3mono-large

def to_numpy(x):
    if torch.is_tensor(x):
        return x.detach().float().cpu().numpy()
    return np.asarray(x)

def colorize_depth(depth):
    depth = to_numpy(depth)
    depth = np.squeeze(depth).astype(np.float32)
    depth = np.nan_to_num(depth)

    depth = cv2.GaussianBlur(depth, (5, 5), 0)

    d_min = np.percentile(depth, 1)
    d_max = np.percentile(depth, 99)

    if d_max - d_min < 1e-6:
        depth_norm = np.zeros_like(depth, dtype=np.uint8)
    else:
        depth = np.clip(depth, d_min, d_max)
        depth_norm = ((depth - d_min) / (d_max - d_min) * 255).astype(np.uint8)

    return cv2.applyColorMap(depth_norm, cv2.COLORMAP_INFERNO)

print("Loading model:", MODEL_NAME)
model = DepthAnything3(model_name=MODEL_NAME).to("cuda").eval()
print("Model loaded.")

cap = cv2.VideoCapture(CAM_ID)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    raise RuntimeError("Camera open failed")

fps_smooth = 0.0
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    t0 = time.time()
    with torch.no_grad():
        pred = model.inference(
            image=[rgb],
            process_res=PROCESS_RES,
            process_res_method="upper_bound_resize",
            infer_gs=False,
            export_dir=None,
        )
    torch.cuda.synchronize()

    dt = time.time() - t0
    fps = 1.0 / dt if dt > 0 else 0
    fps_smooth = fps if fps_smooth == 0 else fps_smooth * 0.9 + fps * 0.1

    depth = pred.depth[0]
    depth_np = to_numpy(depth)

    if frame_count % 30 == 0:
        print(
            "depth shape:", depth_np.shape,
            "min:", float(np.nanmin(depth_np)),
            "max:", float(np.nanmax(depth_np)),
            "range:", float(np.nanmax(depth_np) - np.nanmin(depth_np)),
        )

    depth_vis = colorize_depth(depth)
    depth_vis = cv2.resize(depth_vis, (frame.shape[1], frame.shape[0]))

    cv2.putText(frame, f"RGB | res={PROCESS_RES}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(depth_vis, f"{MODEL_NAME} | FPS={fps_smooth:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    combined = np.hstack([frame, depth_vis])
    cv2.imshow("DA3 Live Depth", combined)

    frame_count += 1

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
