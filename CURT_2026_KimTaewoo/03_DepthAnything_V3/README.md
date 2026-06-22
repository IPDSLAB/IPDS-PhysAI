# Depth Anything V3

> Tested on Jetson Orin NX 16GB + JetPack 6.2.2 + CUDA 12.6

## Objective

Jetson Orin NX 환경에서 Depth Anything V3를 실행하고 실시간 Webcam 기반 Depth Estimation, Autofocus Demo 및 Robot Vision 응용 가능성을 검증한다.

---

## Environment

### Hardware

- Jetson Orin NX 16GB
- Logitech C922 Webcam

### Software

- JetPack 6.2.2
- Jetson Linux R36.5.0
- CUDA 12.6
- Python 3.10.12

---

## Project Goal

본 프로젝트의 목표는 단순히 Depth Map을 생성하는 것이 아니라 실시간 Depth 정보를 활용하여 Autofocus 및 Robot Vision 응용 가능성을 검증하는 것이다.

---

# Environment Setup

## Repository Setup

Depth Anything V3 환경을 구축하였다.

```bash
git clone <Depth-Anything-3 Repository>
cd Depth-Anything-3
```

필요한 Python 패키지 및 모델을 설치하였다.

---

## CUDA Verification

CUDA 환경을 확인하였다.

```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

정상적으로 GPU 사용이 가능함을 확인하였다.

---

# Single Image Inference

## Initial Test

먼저 단일 이미지 추론을 수행하였다.

확인 항목:

- Depth Map 생성
- Confidence Map 생성
- Camera Intrinsics 출력
- Camera Extrinsics 출력

정상적으로 추론 결과가 생성되는 것을 확인하였다.

---

## Result

생성 결과:

- Depth
- Confidence
- Intrinsics
- Extrinsics

Depth Anything V3가 Jetson 환경에서 정상 동작함을 확인하였다.

---

# Real-Time Webcam Demo

## Webcam Verification

Logitech C922 Webcam 연결 후 장치 인식 여부를 확인하였다.

```bash
ls /dev/video*
```

결과:

```text
/dev/video0
/dev/video1
```

주 사용 장치는 `/dev/video0`으로 설정하였다.

---

## First Live Demo

초기 버전에서는 다음 기능을 구현하였다.

- RGB 영상 출력
- Depth 영상 출력
- 실시간 추론

사용 모델:

```python
DepthAnything3(model_name="da3-small")
```

---

## Performance Optimization

Jetson 환경에서 실시간 동작을 위해 추론 해상도 및 추론 주기를 조정하였다.

예시:

```python
PROCESS_RES = 512
INFER_EVERY = 2
```

설정 의미:

- PROCESS_RES : 추론 해상도
- INFER_EVERY : 추론 주기

---

## FPS Monitoring

실시간 성능 확인을 위해 FPS 측정 기능을 추가하였다.

출력 항목:

- Camera FPS
- Inference FPS

실시간 추론 성능을 확인할 수 있도록 구현하였다.

---

# Autofocus Demo

## Motivation

단순히 Depth Map을 시각화하는 수준을 넘어 실제 응용 가능성을 검증하기 위해 Autofocus Demo를 구현하였다.

---

## Center ROI Selection

영상 중앙에 ROI(Region of Interest)를 설정하였다.

중앙 영역의 평균 Depth 값을 계산하도록 구현하였다.

```python
center_depth = np.nanmean(roi)
```

---

## Real-Time Distance Monitoring

실시간으로 중앙 ROI(Region of Interest)의 평균 Depth 값을 측정하였다.

예시:

```text
Center Depth : 1.14
Center Depth : 1.32
Center Depth : 1.58
```

대상 물체의 이동에 따라 Depth 값이 변화하는 것을 확인하였다.

다만 측정값이 실제 거리와 정확히 일치하지는 않았으며, 조명 환경, 카메라 노이즈, 단안 깊이 추정 모델의 한계 등에 의해 값의 변동이 발생하였다.

따라서 본 실험에서는 절대 거리 측정보다는 상대적인 거리 변화 감지의 가능성을 확인하는 데 의의를 두었다.

예를 들어 물체가 카메라에 가까워질수록 Depth 값이 감소하고, 멀어질수록 증가하는 경향을 확인할 수 있었다.

향후에는 실제 거리와의 오차 분석, 카메라 캘리브레이션, ROI 크기 최적화, 모델 성능 개선 등을 통해 보다 정확한 거리 추정이 가능하도록 추가 연구가 필요하다.

---

## Result

중앙 ROI의 Depth 변화가 안정적으로 측정되었으며, 단안 카메라 기반 실시간 거리 변화 감지 가능성을 확인하였다.

다만 현재 단계에서는 정밀한 거리 측정보다는 상대적인 거리 변화 검출 수준에 머물러 있으며, 실제 Autofocus 시스템에 적용하기 위해서는 추가적인 정확도 검증이 필요하다.

그럼에도 불구하고 Jetson Orin NX 환경에서 실시간으로 Depth 값을 추론하고 활용할 수 있음을 확인하였으며, Autofocus 및 Robot Vision 응용 가능성을 검증할 수 있었다.

---

# Data Export

## Save Function

추론 결과 저장 기능을 구현하였다.

저장 항목:

- RGB Image
- Depth Image
- Raw Depth
- Confidence
- Intrinsics
- Extrinsics
- Center Depth

저장 방식:

```python
np.savez_compressed(...)
```

---

## Result

실험 결과를 저장하여 이후 분석에 활용할 수 있도록 하였다.

---

# Model Comparison

## Tested Models

다양한 모델을 비교하였다.

| Model | Speed | Quality |
|---------|---------|---------|
| DA3-SMALL | ★★★★★ | ★★☆☆☆ |
| DA3-BASE | ★★★★☆ | ★★★☆☆ |
| DA3-LARGE | ★★★☆☆ | ★★★★☆ |
| DA3MONO-LARGE | ★★☆☆☆ | ★★★★★ |

---

## Observation

### DA3-SMALL

장점:

- 높은 FPS
- 안정적인 실시간 동작

단점:

- 세부 구조 표현 한계

---

### DA3-BASE

장점:

- 속도와 품질의 균형

예상되는 실시간 응용 모델

---

### DA3MONO-LARGE

장점:

- 가장 우수한 Depth 품질

단점:

- 실시간 응용에는 높은 연산량 요구

---

# Real-Time V3 Wrapper Attempt

## Motivation

실시간 V3 환경을 보다 확장하기 위해 ROS2 기반 Wrapper 프로젝트 적용을 시도하였다.

사용 프로젝트:

- GerdsenAI Depth Anything 3 ROS2 Wrapper

목표:

- ROS2 Camera Node 연동
- TensorRT 활용
- 실시간 V3 추론
- Robot Vision 환경 구축

---

# Docker Environment Setup

## Docker Installation

Jetson 환경에서 Wrapper 실행을 위해 Docker 환경을 구축하였다.

완료 항목:

- Docker 설치
- Docker Compose 설치
- NVIDIA Container Toolkit 설치
- NVIDIA Runtime 등록

---

## Result

Docker 내부에서 GPU 사용이 가능하도록 환경을 구성하였다.

---

# ARM64 Compatibility Issue

## Problem

초기 Docker 이미지 빌드 과정에서 ARM64 관련 문제가 발생하였다.

원인:

- 일부 Base Image가 x86_64 기준으로 작성됨

---

## Solution

Dockerfile을 수정하여 ARM64 환경에 맞게 적용하였다.

수정 후 ARM64 환경에서 빌드가 정상 진행되는 것을 확인하였다.

---

# ROS2 Dependency Analysis

## ROS Key Issue

ROS Repository Key 관련 문제가 발생하였다.

조치:

- ROS Key 수정
- Repository 재설정

정상적으로 패키지 다운로드가 가능해졌다.

---

## ROS Package Installation

설치 대상 패키지:

- ros-humble-cv-bridge
- ros-humble-image-transport
- ros-humble-v4l2-camera
- ros-humble-vision-opencv

---

# OpenCV Dependency Conflict

## Problem

Docker 빌드 과정에서 OpenCV 개발 패키지 설치 단계에서 오류가 발생하였다.

대표 오류:

```text
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

---

## Analysis

다음 패키지들이 설치 과정에서 충돌하였다.

- libopencv-core-dev
- libopencv-imgproc-dev
- libopencv-highgui-dev
- libopencv-contrib-dev
- libopencv-dev

추가 분석 결과 `ros-humble-cv-bridge`가 OpenCV 개발 패키지를 의존성으로 포함하고 있으며, Jetson ARM64 환경에서 충돌이 발생하는 것으로 판단하였다.

---

## Decision

실시간 Wrapper 포팅은 일시 중단하고 안정적으로 동작하는 원본 V3 환경 유지에 집중하였다.

---

# Python Environment Issue

## Problem

V2 재실행 과정에서 다음 오류가 발생하였다.

```text
ModuleNotFoundError: No module named 'torch'
```

---

## Cause

Conda Base 환경에서 실행하고 있었으며 해당 환경에는 PyTorch가 설치되어 있지 않았다.

실행 환경:

```text
(base) pdpd@pdpd-desktop1
```

---

## Solution

```bash
conda deactivate
```

이후 정상 Python 환경으로 전환하여 실행하였다.

---

# Current Status

## Completed

- Depth Anything V3 설치
- 단일 이미지 추론 성공
- Webcam 실시간 추론 성공
- Autofocus Demo 구현
- Center Depth 측정
- Depth 저장
- Confidence 저장
- Intrinsics 저장
- Extrinsics 저장
- Docker 설치
- NVIDIA Runtime 등록
- ARM64 이미지 수정
- ROS Key 문제 해결

---

## In Progress

- GerdsenAI ROS2 Wrapper 포팅
- TensorRT 기반 실시간화

---

## Current Blocking Issue

- OpenCV / cv_bridge 의존성 충돌

---

# Application Possibilities

## Autofocus System

- 실시간 거리 측정
- 자동 초점 제어

## Robot Vision

- 객체 거리 추정
- 장애물 인식

## 3DGS Preprocessing

- 초기 Depth 정보 생성
- Scene Reconstruction 보조

## Medical Imaging Assistance

- 환자 움직임 추적
- 모션 보정 보조

---

# Lessons Learned

- 단순 Depth 시각화보다 실제 거리값 활용이 중요하다.
- DA3-SMALL은 실시간 응용에 적합하다.
- ROI 기반 평균 Depth 측정은 Autofocus 응용에 효과적이다.
- Docker 및 ROS2 환경 구축 과정에서 ARM64 호환성 문제가 발생할 수 있다.
- OpenCV 의존성 문제는 Jetson 환경에서 중요한 이슈가 될 수 있다.
- Jetson Orin NX에서도 실시간 Depth AI 응용이 가능함을 확인하였다.

---

# Future Work

- DA3-BASE 성능 검증
- TensorRT 최적화
- ROS2 Wrapper 완성
- Robot Vision 적용
- 3DGS 파이프라인 연동
- Autofocus 시스템 연동
