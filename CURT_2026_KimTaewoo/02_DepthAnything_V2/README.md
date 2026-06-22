# Depth Anything V2

## Objective

Jetson Orin NX 환경에서 Depth Anything V2를 설치하고, Logitech C922 웹캠을 이용한 실시간 Depth Estimation을 수행한다.

---

## Environment

### Hardware

* Jetson Orin NX 16GB
* Logitech C922 Webcam

### Software

* JetPack 6.2.2
* Jetson Linux R36.5.0
* CUDA 12.6
* Python 3.10.12
* Depth Anything V2

---

## Repository Setup

Depth Anything V2 저장소를 Jetson 환경에 설치하였다.

```bash
cd ~
git clone https://github.com/DepthAnything/Depth-Anything-V2.git
cd Depth-Anything-V2
```

---

## Webcam Test

Logitech C922 웹캠이 정상적으로 인식되는지 확인하였다.

```bash
ls /dev/video*
```

확인 결과 `/dev/video0`, `/dev/video1` 장치가 생성되었다.

주 사용 장치는 `/dev/video0`으로 설정하였다.

---

## Real-Time Depth Estimation

웹캠 기반 실시간 Depth Estimation을 위해 `webcam_depth.py`를 실행하였다.

```bash
cd ~/Depth-Anything-V2
python3 webcam_depth.py
```

해당 코드는 웹캠 입력 영상을 받아 RGB 영상과 Depth Map을 실시간으로 출력하는 데 사용하였다.

---

## Issue: PyTorch Module Not Found

실행 과정에서 다음 오류가 발생하였다.

```text
ModuleNotFoundError: No module named 'torch'
```

### Cause

당시 터미널 환경이 Conda base 환경으로 설정되어 있었다.

```text
(base) pdpd@pdpd-desktop1:~/Depth-Anything-V2$
```

해당 Conda base 환경에는 PyTorch가 설치되어 있지 않아 `torch` 모듈을 찾지 못하였다.

### Solution

Conda base 환경을 비활성화하였다.

```bash
conda deactivate
```

이후 프롬프트에서 `(base)` 표시가 사라진 것을 확인한 뒤 다시 실행하였다.

```bash
cd ~/Depth-Anything-V2
python3 webcam_depth.py
```

---

## Result

Depth Anything V2를 Jetson Orin NX 환경에서 실행하였고, Logitech C922 웹캠 기반 실시간 Depth Estimation을 수행하였다.

확인된 내용:

* Logitech C922 웹캠 인식
* `/dev/video0` 입력 사용
* Depth Anything V2 실행
* 실시간 RGB / Depth 출력
* RGB 및 Depth 결과 저장 가능

---

## Lessons Learned

* Jetson 환경에서는 Python 실행 환경 확인이 중요하다.
* Conda base 환경과 시스템 Python 환경이 다를 경우 패키지 충돌이 발생할 수 있다.
* `ModuleNotFoundError: No module named 'torch'` 오류는 PyTorch 미설치뿐 아니라 잘못된 Python 환경에서 실행했을 때도 발생할 수 있다.
* 실행 전 `conda deactivate`를 통해 올바른 환경에서 실행하는 것이 필요하다.
