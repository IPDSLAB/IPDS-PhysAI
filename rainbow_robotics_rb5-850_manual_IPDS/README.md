# rainbow_robotics_rb5-850_manual

Rainbow Robotics **RB5-850** 한팔(6축) 협동로봇 프로그래밍을 위한 기초 예제 모음입니다.
처음 다루는 사용자가 코드 제어를 학습할 수 있도록 정리했습니다.

> ⚠️ **읽기 전용 폴더 (Read-Only)**
> 이 디렉토리는 [@yeramonster](https://github.com/yeramonster)의 개인 리포지토리와 자동 동기화됩니다.
> 공동 리포지토리에서 직접 수정할 경우 동기화 과정에서 내용이 삭제되거나 꼬일 수 있으니,
> 수정이 필요하면 반드시 관리자에게 문의해 주세요.

---

## 📂 폴더 구조

```
rainbow_robotics_rb5-850/
├── basics/                     # 기초 동작 예제
│   ├── go_home.py              # 홈 좌표로 이동
│   ├── rbpodo_ex1.py           # 실시간 위치 전송
│   ├── rbpodo_ex2.py           # move_l (직선 이동)
│   └── rbpodo_ex3.py           # move_j (관절 이동)
├── cobot_api/                  # rainbow cobot API 예제
│   ├── cobot_pose_head.py      # cobot 라이브러리 import 헤더
│   └── cobot_pose_test.py      # 지정한 5개 pose 반복 동작
├── docs/                       # 문서
│   ├── coordinate_system.md    # move_j / move_l 좌표계 설명
│   ├── error_troubleshooting.md# 로봇이 멈췄을 때 대처법
│   └── RB5-850_고려대_메뉴얼_구성훈.pdf  # 운용 인수인계서
├── setup/
│   └── network_config.md       # IP 고정, 포트 설정 가이드
└── README.md
```

---

## 🚀 시작하기

### 1. 환경

- Python 3.x
- `rbpodo` 라이브러리 — [RainbowRobotics/rbpodo](https://github.com/RainbowRobotics/rbpodo)
- `rb-api-python` (cobot API 사용 시) — [PyPI](https://pypi.org/project/rb-api-python/)
  ```python
  from rainbow import cobot
  ```

### 2. 네트워크 연결

코드를 실행하기 전 PC와 로봇 컨트롤 박스가 유선 LAN으로 연결되어 있어야 합니다.
자세한 설정은 [setup/network_config.md](setup/network_config.md)를 참고하세요.

```python
ROBOT_IP = "172.16.3.128"  # 308호 로봇암 주소 (환경에 따라 다름, 사용 전 확인)
```

> 사용 환경에 따라 IP가 다를 수 있습니다. 인수인계서 기준 외부 제어용 컨트롤 박스 IP는
> `10.0.2.7` (명령 포트 5000 / 상태 포트 5001)입니다. 실제 환경에서 확인 후 사용하세요.

---

## 🤖 동작 명령 기본 (move_j / move_l)

티치 펜던트 우측 상단에 표시되는 두 좌표:

- **왼쪽 좌표** → `move_l` 에 사용 (직교 좌표)
- **오른쪽 좌표** → `move_j` 에 사용 (관절 각도)

| 명령 | 입력값 | 특징 |
|------|--------|------|
| **move_j** | 관절 각도 6개 (J0~J5) | 6개 관절이 동시에 움직임. 특이점에 강함. **주로 사용** |
| **move_l** | X, Y, Z, RX, RY, RZ | TCP가 직선 이동. A, B, C 축 회전 → rx, ry, rz |

> 좌표계 상세 설명은 [docs/coordinate_system.md](docs/coordinate_system.md) 참고

---

## 📄 코드 파일 설명

| 파일 | 설명 |
|------|------|
| `basics/rbpodo_ex1.py` | 실시간 위치 전송 |
| `basics/rbpodo_ex2.py` | **move_l** — 기존 좌표에서 `target_point = np.array([x, y, z, rx, ry, rz])` 의 입력값만큼 + 방향으로 이동 |
| `basics/rbpodo_ex3.py` | **move_j** — `joint = np.array([base, shoulder, elbow, wrist1, wrist2, wrist3])` 입력값으로 이동 |
| `cobot_api/cobot_pose_head.py` | `cobot_pose_test.py` 에서 사용하는 cobot 라이브러리 import 파일 |
| `cobot_api/cobot_pose_test.py` | 코드 내 지정한 5개 pose(1~5)를 반복 동작 (move_l 좌표 사용) |

> `rbpodo_ex1~3.py` 는 rbpodo GitHub 예제와 기본 구조가 동일합니다.

---

## 📚 공식 매뉴얼 (Rainbow Robotics)

본 리포지토리는 학습용 예제이며, 정확한 사양·안전 정보는 제조사 공식 매뉴얼을 따르세요.

- **온라인 매뉴얼 (RB Series)**: https://rainbowrobotics.github.io/rb_cobot_docs/ko/
- **매뉴얼/소프트웨어 다운로드**: https://www.rainbow-robotics.com/download
- **제조사 홈페이지**: https://www.rainbow-robotics.com
- **rbpodo GitHub**: https://github.com/RainbowRobotics/rbpodo

### 자주 보는 챕터 바로가기

| 주제 | 링크 |
|------|------|
| 협동로봇 시스템 개요 | [1.1 협동로봇 시스템](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/product_introduction/cobot_system) |
| 안전 / 비상정지 | [2.7 비상 정지](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/safety_and_precautions/emc_stop) |
| 로봇 구동하기 | [8.1 로봇 구동하기](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/starting_the_robot/robot_operation) |
| 운용 중 특이사항 대처 | [8.3 운용중 발생한 특이사항 대처](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/starting_the_robot/troubleshooting_while_operating) |
| 외부 스크립트 제어 API | [부록 E. 외부 스크립트 제어 API](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/appendix/ext_script_api) |
| 좌표계 설정 | [부록 F. 좌표계 설정](https://rainbowrobotics.github.io/rb_cobot_docs/ko/manual/appendix/coordinate_system) |

---

## ⚠️ 안전 주의사항

- 새 동작은 반드시 **Simulation 모드**로 먼저 검증 후 Real 모드로 구동
- 구동 전 주변 사람·장애물 확인, 비상정지 스위치 위치 숙지
- 툴 부하(Load) 세팅 필수 — 미설정 시 직접교시·충돌감지 오작동
- 로봇 연결 중 **VPN / 네트워크 변경 금지** (코드 즉시 먹통)
- `task stop` 은 급정지 유발 → 가능하면 `task pause` 후 정지

로봇이 멈췄을 때 대처법은 [docs/error_troubleshooting.md](docs/error_troubleshooting.md)를 참고하세요.
