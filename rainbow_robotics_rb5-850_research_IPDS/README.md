# rainbow_robotics_rb5-850_research

Rainbow Robotics RB5-850 협동로봇을 활용한 연구·실험 프로젝트 모음입니다.
본 저장소는 **연구 기록 및 정보 공유·보관**을 목적으로 공개되어 있습니다.

---

## ⚠️ 이용 안내 (Notice)

본 저장소의 모든 코드와 문서는 **열람·참고 전용**입니다.

- 📖 **참고용입니다.** 코드 구조, 접근 방식, 구현 아이디어를 참고하는 용도로만 공개합니다.
- 🚫 **실행/구동을 위한 것이 아닙니다.** 본 코드는 특정 하드웨어 환경(아래 환경 참조)에 맞춰 작성되었으며, 그대로 실행하는 것을 전제로 하지 않습니다.
- 🤖 **실제 로봇 구동 위험.** 협동로봇 제어 코드를 검증 없이 실행할 경우 장비 손상 및 안전사고가 발생할 수 있습니다. 본 코드 실행으로 인한 어떠한 문제에 대해서도 작성자는 책임지지 않습니다.

> 본 저장소의 코드를 사용하고자 하는 경우 반드시 작성자에게 사전 문의하시기 바랍니다.

---

## 🛠 개발 환경 (Environment)

### 로봇
- **Rainbow Robotics RB5-850** 협동로봇
- 제어 라이브러리: `rbpodo`
- IP: `172.16.3.128`

### 카메라
- **Canon EOS R8** (미러리스)
- 렌즈: Canon RF 85mm F2 Macro IS STM
- 제어 라이브러리: `gphoto2`
- 연결: USB 테더링

### 컴퓨터
- OS: Ubuntu 22.04
- IDE: VS Code
- 언어: Python (가상환경 `venv`)

---

## 📂 저장소 구성 (Structure)

본 저장소는 RB5-850을 활용한 여러 연구 프로젝트를 폴더 단위로 보관합니다.

| 프로젝트 | 개요 |
|----------|------|
| **GigaPixelArt** | 2D 회화 작품 자동 근접 촬영 + 스티칭 기반 기가픽셀 디지털화 |
| **MetricScan** | Hand-Eye 캘리브레이션 기반 실제 크기(실척) 3D 복원 |

> 각 프로젝트의 상세 내용은 별도 문서로 관리되며, 본 README에서는 다루지 않습니다.

---

## 📌 기타

- 본 저장소는 연구 진행에 따라 비정기적으로 업데이트됩니다.
- 문의: 작성자(저장소 소유자)에게 연락 바랍니다.

---

*This repository is published for research documentation and reference purposes only.
Unauthorized use, reproduction, distribution, or execution of the code is not permitted.*
