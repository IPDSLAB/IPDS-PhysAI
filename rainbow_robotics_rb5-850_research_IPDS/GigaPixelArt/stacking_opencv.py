import cv2
import numpy as np
import glob
import os

# =========================
# 1. 이미지 로드
# =========================
input_dir = "stack_images_hangul"   # 너 촬영 폴더
output_file = "stacked_result_hangul.jpg"

files = sorted(glob.glob(os.path.join(input_dir, "*.jpg")))
imgs = [cv2.imread(f) for f in files]

if len(imgs) == 0:
    raise Exception("이미지가 없습니다. 폴더 확인하세요.")

print(f"Loaded {len(imgs)} images")

# =========================
# 2. ALIGNMENT (ECC)
# =========================
aligned_imgs = []

ref_gray = cv2.cvtColor(imgs[0], cv2.COLOR_BGR2GRAY)
aligned_imgs.append(imgs[0])

warp_mode = cv2.MOTION_EUCLIDEAN
warp_matrix_init = np.eye(2, 3, dtype=np.float32)

criteria = (
    cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
    50,
    1e-6
)

print("Aligning images...")

for i in range(1, len(imgs)):

    img_gray = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2GRAY)

    warp_matrix = warp_matrix_init.copy()

    try:
        _, warp_matrix = cv2.findTransformECC(
            ref_gray,
            img_gray,
            warp_matrix,
            warp_mode,
            criteria
        )

        aligned = cv2.warpAffine(
            imgs[i],
            warp_matrix,
            (imgs[i].shape[1], imgs[i].shape[0]),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        )

    except:
        # alignment 실패 시 원본 사용
        aligned = imgs[i]

    aligned_imgs.append(aligned)

print("Alignment done")

# =========================
# 3. FOCUS STACKING (Fusion)
# =========================

print("Fusing images...")

h, w, _ = aligned_imgs[0].shape

result = np.zeros((h, w, 3), dtype=np.float32)
weight_sum = np.zeros((h, w), dtype=np.float32)

def focus_measure(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F)

for img in aligned_imgs:

    sharp = np.abs(focus_measure(img))

    # 안정화 (noise 제거)
    weight = cv2.GaussianBlur(sharp, (11, 11), 0)

    # normalize (중요)
    weight = weight / (np.max(weight) + 1e-6)

    for c in range(3):
        result[:, :, c] += img[:, :, c] * weight

    weight_sum += weight

# normalize final
result = result / (weight_sum[:, :, None] + 1e-6)

result = np.clip(result, 0, 255).astype(np.uint8)

# =========================
# 4. 저장
# =========================

cv2.imwrite(output_file, result)

print(f"Done -> {output_file}")
