# CURT 2026 - Jetson Orin NX & Depth Anything

## Project Overview

본 프로젝트에서는 Jetson Orin NX 환경에서 단안 깊이 추정(Monocular Depth Estimation) 모델인 Depth Anything V2 및 V3를 Jetson 환경에 포팅하고 실시간 추론 환경을 구축하는 것을 목표로 하였다.

Windows 기반 Host PC를 이용하여 Jetson Orin NX 개발 환경을 구축하였으며, JetPack 6.2.2 및 CUDA 12.6 환경에서 실시간 Webcam 기반 Depth Estimation을 수행하였다. 또한 단순 모델 실행을 넘어 실시간 추론 최적화, 데이터 저장, Autofocus 응용 가능성 검증 및 ROS2 기반 확장 가능성을 탐색하였다.

---

## My Contribution

### 1. Jetson Orin NX Development Environment Setup

* BIOS Virtualization 활성화
* WSL2 및 Ubuntu 환경 구축
* NVIDIA SDK Manager 설치
* JetPack 6.2.2 플래싱
* CUDA 12.6 개발 환경 구성
* 네트워크 및 패키지 설치 문제 해결
* Logitech C922 Webcam 연동
* Jetson 개발 환경 검증

### 2. Depth Anything V2

* 모델 설치 및 환경 구성
* 단일 이미지 추론 검증
* Webcam 기반 실시간 Depth Estimation 구현
* Depth Map 생성 및 시각화
* 추론 결과 저장 기능 구현

### 3. Depth Anything V3

* 모델 설치 및 환경 구성
* CUDA 기반 추론 검증
* Webcam 기반 실시간 Depth Estimation 구현
* DA3-SMALL / DA3MONO-LARGE 모델 비교
* 실시간 추론 성능 최적화
* Autofocus Demo 구현
* Center ROI 기반 거리 변화 측정
* Docker 및 ROS2 Wrapper 적용 시도

---

## Repository Structure

```text
CURT_2026_KimTaewoo
│
├── README.md
├── 01_Jetson_OrinNX_Setup
├── 02_DepthAnything_V2
├── 03_DepthAnything_V3
└── Images
```

---

## Development Environment

### Hardware

* Jetson Orin NX 16GB
* Logitech C922 Webcam

### Software

* Ubuntu 22.04
* JetPack 6.2.2
* Jetson Linux R36.5.0
* CUDA 12.6
* Python 3.10.12

---

## Project Images

### Jetson Orin NX Environment Setup

Jetson Orin NX 개발 환경 구축 및 Ubuntu 환경 구성

### Depth Anything V2 Real-Time Demo

Webcam 기반 실시간 Depth Estimation 실행 결과

### Depth Anything V3 Real-Time Demo

Depth Anything V3를 이용한 실시간 Depth Estimation 실행 결과

---

## Current Status

### Completed

* Jetson Orin NX Environment Setup
* JetPack 6.2.2 Installation
* CUDA 12.6 Verification
* Webcam Recognition Test
* Depth Anything V2 Execution
* Depth Anything V3 Execution
* Real-Time Webcam Testing
* Autofocus Demo Implementation
* Data Export Function
* Docker Environment Setup

### In Progress

* ROS2 Wrapper Integration
* TensorRT Optimization
* Additional Performance Validation

---

## Results

Jetson Orin NX 환경에서 Depth Anything V2 및 V3 실행에 성공하였으며, Webcam 기반 실시간 Depth Estimation 환경을 구축하였다.

또한 ROI 기반 거리 변화 측정을 통해 Autofocus 응용 가능성을 검증하였으며, Docker 및 ROS2 Wrapper 적용을 통해 Robot Vision 확장 가능성을 확인하였다.

---

## Future Work

* TensorRT 최적화
* ROS2 Wrapper 완성
* Robot Vision 적용
* 3DGS 파이프라인 연동
* Autofocus 시스템 연동
* 실측 거리 기반 성능 평가
