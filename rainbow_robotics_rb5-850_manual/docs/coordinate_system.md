# 좌표계 및 동작 명령 가이드

## Move J vs Move L 비교

| 항목 | Move J (조인트) | Move L (리니어) |
|------|----------------|----------------|
| 입력값 | 관절 각도 6개 (J0~J5) | X, Y, Z, RX, RY, RZ |
| 경로 | 비직선 (관절 회전) | TCP 직선 이동 |
| 특이점 | 강함 (통과 가능) | 약함 (특이점 근처 급격한 속도 발생) |
| 주 용도 | 자세 이동, 일반 동작 | 직선 삽입, 면 따라 이동 |
| 우리 현장 | ✅ 주로 사용 | 필요 시만 사용 |

## Move J 좌표 읽는 법

티치 펜던트 우측 상단에 두 좌표가 표시됩니다.

- **왼쪽 좌표** → `move_l` 에 사용되는 직교 좌표 (X, Y, Z, RX, RY, RZ)
- **오른쪽 좌표** → `move_j` 에 사용되는 관절 각도 (J0~J5)

## 관절 구성 (J0~J5)

    joint = [J0,   J1,       J2,    J3,      J4,      J5    ]
          = [Base, Shoulder, Elbow, Wrist1,  Wrist2,  Wrist3]

예시:

```python
# 기준 패킹 자세 (운반/복구 시 사용)
home = [90, -65, 155, -45, -90, 0]  # 단위: degree
```

## Move L 좌표계

    target = [X,   Y,   Z,   RX,  RY,  RZ ]
           = [mm,  mm,  mm,  deg, deg, deg]

- X / Y / Z : TCP의 3차원 위치 (밀리미터)
- RX / RY / RZ : TCP의 회전 (A, B, C 축 — 도(degree) 단위)

## 특이점(Singular Point) 주의

베이스 바로 위/아래 영역에서 Move L 사용 시:

- 관절이 갑자기 빠르게 움직이거나 정지할 수 있음
- **이 영역에서는 반드시 Move J 사용**

## 코드 예시

```python
import numpy as np

# Move J — 관절 각도로 이동
joint = np.array([0, -65, 155, -45, -90, 0])  # J0~J5 (degree)

# Move L — 현재 위치 기준 상대 이동
delta = np.array([100, 0, 0, 0, 0, 0])  # X방향으로 100mm 이동
```
