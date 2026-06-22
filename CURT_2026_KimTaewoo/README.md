# CURT 2026 - Jetson Orin NX & Depth Anything

## Project Overview

본 프로젝트에서는 Jetson Orin NX 환경에서 단안 깊이 추정(Monocular Depth Estimation) 모델인 Depth Anything V2 및 V3를 설치하고 실행하는 것을 목표로 하였다.

Windows 기반 Host PC를 이용하여 Jetson Orin NX 개발 환경을 구축하고, JetPack 및 CUDA 환경 구성 후 실시간 카메라 기반 Depth Estimation 동작을 검증하였다.

---

## My Contribution

### 1. Jetson Orin NX Development Environment Setup

* WSL2 및 Ubuntu 환경 구축
* NVIDIA SDK Manager 설치
* JetPack 설치 및 플래싱
* Ubuntu 개발 환경 구성
* Webcam 인식 테스트
* 개발 환경 검증

### 2. Depth Anything V2

* 모델 설치
* 예제 실행
* Depth Map 생성 검증

### 3. Depth Anything V3

* 모델 설치
* Webcam 연동
* 실시간 Depth Estimation
* 추론 최적화

---

## Repository Structure

```text
CURT_2026_KimTaewoo

├─ README.md

├─ 01_Jetson_OrinNX_Setup

├─ 02_DepthAnything_V2

├─ 03_DepthAnything_V3

└─ Images
```

---

## Development Environment

### Hardware

* Jetson Orin NX 16GB
* Logitech C922 Webcam

### Software

* Ubuntu 22.04
* JetPack 6.x
* CUDA 12.x
* Python 3.10

---

## Current Status

### Completed

* Jetson Orin NX Environment Setup
* JetPack Installation
* Webcam Recognition
* Depth Anything V2 Execution
* Depth Anything V3 Execution
* Real-Time Webcam Testing

### Ongoing

* Documentation
* Performance Optimization
* Additional Validation

---

## Results

Jetson Orin NX 환경에서 Depth Anything V2 및 V3 실행에 성공하였으며, 실시간 Webcam 기반 Depth Estimation 환경을 구축하였다.
