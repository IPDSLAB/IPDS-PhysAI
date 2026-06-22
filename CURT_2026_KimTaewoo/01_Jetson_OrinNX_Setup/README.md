# Jetson Orin NX Setup

## Objective

Jetson Orin NX 환경에서 AI 비전 모델 실행을 위한 개발 환경을 구축한다.

---

## Hardware

* Jetson Orin NX 16GB
* Windows Laptop (Host PC)
* USB Type-C Cable
* Logitech C922 Webcam

---

## Software

* Windows 11
* WSL2 (Windows Subsystem for Linux)
* Ubuntu 22.04 (WSL)
* NVIDIA SDK Manager
* JetPack 6.x
* CUDA 12.x

---

## Environment Preparation

### 1. WSL2 및 Ubuntu 설치

Jetson Orin NX에 JetPack을 설치하기 위해 Windows 환경에서 WSL2를 활성화하였다.

Ubuntu 22.04를 설치한 후 초기 설정을 진행하였다.

초기 실행 시 Metrics Collection 관련 질문이 표시되었으며 정상적인 설치 과정임을 확인하였다.

```text
Would you like to opt-in to platform metrics collection (Y/n)?
```

사용자 계정 및 비밀번호 설정 후 WSL 환경 구성을 완료하였다.

---

### 2. WSL 정상 동작 확인

WSL 환경이 정상적으로 실행되는지 확인하였다.

```bash
user@DESKTOP-XXXX:/mnt/c/WINDOWS/system32$
```

Linux Shell Prompt가 출력되는 것을 확인하여 WSL 환경이 정상적으로 동작함을 검증하였다.

---

## SDK Manager Setup

### 1. NVIDIA SDK Manager 설치

Jetson 개발 환경 구성을 위해 NVIDIA SDK Manager를 설치하였다.

### 2. Jetson Recovery Mode 진입

Jetson Orin NX를 Recovery Mode로 진입시킨 후 USB Type-C 케이블을 이용하여 Host PC와 연결하였다.

### 3. JetPack 설치 설정

SDK Manager에서 다음 항목을 선택하였다.

* Jetson OS : 선택
* Additional SDK : 미선택
* Platform Services : 미선택

이후 JetPack 설치를 진행하였다.

---

## Flashing Process

### 1. 장치 인식 확인

SDK Manager 로그를 통해 Jetson 보드가 정상적으로 인식되는 것을 확인하였다.

```text
Device flash pre launch final sweep has been passed.
Identified 'jetson-orin-nano-devkit' target board.
```

플래싱 시작 전 사전 점검이 완료되었음을 의미한다.

---

### 2. 플래싱 시작

SDK Manager가 Jetson 장치에 Ubuntu 및 JetPack 이미지를 기록하기 시작하였다.

```text
sudo ./nvsdkmanager_flash.sh
```

플래싱 과정 중 Jetson 재부팅 및 재연결 과정이 수행되었다.

---

## Issues Encountered

### Issue 1. WSL 환경 관련 문제

초기 설치 과정에서 SDK Manager가 정상적으로 동작하지 않았다.

#### Solution

* WSL2 설치
* Ubuntu 환경 구성
* SDK Manager 재실행

이후 정상적으로 플래싱이 진행되었다.

---

### Issue 2. Flashing 중 시스템 종료

플래싱 진행 중 Jetson 전원이 갑자기 종료되는 문제가 발생하였다.

사용 전원:

* 12V 5A Adapter

#### Analysis

플래싱 과정에서 시스템 부하가 증가하며 전압 안정성 문제가 발생한 것으로 판단하였다.

Jetson Orin NX는 NVIDIA 권장 전원 사용이 필요하다.

---

### Issue 3. 플래싱 중단 후 Ubuntu 부팅

플래싱 도중 설치가 중단되었으나 Jetson을 재부팅하자 Ubuntu Desktop 환경이 정상적으로 실행되었다.

#### Observation

확인된 사항:

* Ubuntu 부팅 가능
* Desktop 환경 진입 가능
* 사용자 계정 생성 가능

이를 통해 운영체제의 상당 부분이 이미 기록되었음을 확인하였다.

#### Risk

다음과 같은 문제가 발생할 수 있다고 판단하였다.

* CUDA 미설치
* TensorRT 누락
* 드라이버 불완전 설치
* 개발 환경 오류 발생 가능

---

## Post Installation Configuration

### 1. USB Webcam Recognition Test

Logitech C922 USB Webcam 연결 후 장치 인식 여부를 확인하였다.

```bash
ls /dev/video*
```

결과:

```text
/dev/video0
/dev/video1
```

장치가 정상적으로 등록된 것을 확인하였다.

추가적으로 V4L2 장치 정보를 확인하였다.

```bash
v4l2-ctl --list-devices
```

---

### 2. Camera Validation

카메라 동작 여부를 확인하기 위해 OpenCV 기반 테스트를 수행하였다.

주 사용 장치는:

* /dev/video0

실시간 영상 입력이 정상적으로 동작하는 것을 확인하였다.

---

### 3. Package Manager Lock Issue

패키지 설치 과정에서 apt Cache Lock 문제가 발생하였다.

대표적인 증상:

```text
Waiting for cache lock
Could not get lock
```

원인 분석 결과 다른 프로세스가 apt 패키지 관리자를 사용 중인 상태였다.

해결 과정:

```bash
ps aux | grep apt
sudo dpkg --configure -a
sudo apt update
```

---

### 4. Korean Language Environment

Jetson Ubuntu 환경에서 한글 입력 환경 구성을 시도하였다.

#### Language Support

* Korean Language Pack 설치
* Input Method : IBus 설정

#### Hangul Input

```bash
sudo apt install ibus-hangul
```

#### Result

한글 입력 환경 구성을 시도하였으나 정상적으로 동작하지 않았다.

#### Future Work

* IBus 설정 재검토
* Jetson Ubuntu 환경에서의 한글 입력기 호환성 확인
* 추가 설정 검증

---

## Final Result

최종적으로 다음 개발 환경 구축을 완료하였다.

* Ubuntu Desktop
* JetPack
* CUDA
* USB Webcam
* Python 개발 환경

이를 기반으로 이후 Depth Anything V2 및 V3 개발 환경 구축을 진행하였다.

---

## Lessons Learned

* Windows 환경에서도 WSL2를 활용하여 Jetson 개발 환경을 구축할 수 있다.
* SDK Manager 사용 시 WSL 환경이 정상적으로 동작해야 한다.
* Jetson 플래싱 과정에서는 안정적인 전원 공급이 중요하다.
* 플래싱 도중 오류가 발생하더라도 Ubuntu가 부분적으로 설치될 수 있다.
* JetPack 설치 완료 여부는 CUDA 및 개발 환경 검증을 통해 최종 확인해야 한다.
