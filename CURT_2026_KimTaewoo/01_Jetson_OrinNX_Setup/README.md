# Jetson Orin NX Setup

## Objective

Jetson Orin NX 환경에서 AI 비전 모델(Depth Anything)을 실행하기 위한 개발 환경을 구축한다.

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
* Ubuntu 22.04
* NVIDIA SDK Manager
* JetPack 6.x
* CUDA 12.x

---

# Environment Preparation

## 1. BIOS Virtualization Configuration

WSL2 사용을 위해 CPU 가상화 기능이 활성화되어 있어야 한다.

초기 환경 구성 과정에서 BIOS Setup으로 진입하여 가상화 관련 설정을 확인하였다.

확인 항목:

* Intel Virtualization Technology (VT-x)
* Virtualization Support

설정을 저장한 후 시스템을 재부팅하였다.

### Verification

Windows 작업 관리자(Task Manager)를 이용하여 가상화 상태를 확인하였다.

Virtualization : Enabled

가상화 기능이 정상적으로 활성화된 것을 확인하였다.

---

## 2. WSL2 Installation

Jetson SDK Manager 사용을 위해 Windows 환경에 WSL2를 설치하였다.

Ubuntu 22.04 배포판을 다운로드하여 설치하였다.

---

## 3. Ubuntu Initial Setup

Ubuntu 최초 실행 시 다음 설정을 진행하였다.

### Metrics Collection

초기 실행 시 아래와 같은 메시지가 출력되었다.

Would you like to opt-in to platform metrics collection (Y/n)?

이는 Ubuntu 사용 통계 수집 여부를 묻는 항목이며 설치 과정에는 영향을 주지 않는다.

### User Account Setup

* 사용자 계정 생성
* 비밀번호 설정

초기 설정 완료 후 Ubuntu Shell에 진입하였다.

---

## 4. WSL Verification

Ubuntu Shell이 정상적으로 실행되는지 확인하였다.

user@DESKTOP-VNU2DOF:/mnt/c/WINDOWS/system32$

확인 항목:

* BIOS Virtualization
* WSL2
* Ubuntu Distribution

정상 동작 확인.

---

# NVIDIA SDK Manager Setup

## 1. SDK Manager Installation

NVIDIA SDK Manager를 설치하였다.

SDK Manager 실행 시 관리자 권한을 사용하였다.

---

## 2. WSL Related Troubleshooting

초기 설치 과정에서 SDK Manager 관련 오류가 발생하였다.

WSL 상태를 확인하기 위해 다음 명령을 사용하였다.

```powershell
wsl --shutdown
```

WSL 환경을 재시작한 후 SDK Manager를 다시 실행하였다.

---

## 3. Recovery Mode

Jetson Orin NX를 Recovery Mode로 진입시켰다.

이후 USB Type-C 케이블을 이용하여 Host PC와 연결하였다.

---

## 4. JetPack Configuration

SDK Manager에서 다음과 같이 설정하였다.

* Jetson OS : 선택
* Additional SDK : 미선택
* Platform Services : 미선택

설정 완료 후 Install을 진행하였다.

---

# Flashing Process

## Device Detection

SDK Manager 로그를 통해 Jetson 장치 인식을 확인하였다.

Device flash pre launch final sweep has been passed.

Identified 'jetson-orin-nano-devkit' target board.

플래싱 시작 전 사전 점검이 정상적으로 완료된 상태이다.

---

## Flash Start

플래싱이 시작되면서 Ubuntu 및 JetPack 이미지가 Jetson 장치에 기록되기 시작하였다.

sudo ./nvsdkmanager_flash.sh

Jetson 재부팅 및 재연결 과정이 자동으로 수행되었다.

---

# Power Issue During Flashing

## Symptom

플래싱 진행 중 Jetson 전원이 갑자기 종료되는 문제가 발생하였다.

당시 사용 전원:

* 12V 5A Adapter

발생 증상:

* 플래싱 중단
* Jetson 전원 종료
* SDK Manager 오류 발생

---

## Analysis

플래싱 과정에서 시스템 부하가 증가하면서 전압 안정성 문제가 발생한 것으로 판단하였다.

전류 용량은 충분했지만 NVIDIA 권장 전압보다 낮은 전원을 사용하고 있었다.

---

## Unexpected Result

플래싱 실패 후 Jetson을 다시 부팅하자 Ubuntu Desktop 환경이 정상적으로 실행되었다.

확인된 내용:

* Ubuntu Desktop 진입 가능
* 로그인 가능
* 사용자 계정 생성 가능

이를 통해 운영체제 이미지 일부 또는 대부분이 이미 기록되었음을 확인하였다.

---

## Risk Assessment

다만 다음과 같은 문제가 발생할 수 있다고 판단하였다.

* CUDA 누락
* TensorRT 누락
* JetPack 구성 요소 누락
* 드라이버 불완전 설치

따라서 이후 JetPack 설치를 다시 진행하여 개발 환경을 완성하였다.

---

# Network Troubleshooting

## Initial Network Issue

Jetson Ubuntu 부팅 후 학교 건물 내 벽면 LAN 포트를 이용하여 인터넷 연결을 시도하였으나 정상적으로 인터넷을 사용할 수 없었다.

확인된 사항:

* Ethernet 인터페이스 인식 정상
* 랜 케이블 연결 정상
* 물리적 링크 연결 정상
* 인터넷 접속 불가

---

## Network Verification

네트워크 상태를 확인하기 위해 다음 명령어를 사용하였다.

```bash
ping -c 4 8.8.8.8
ping -c 4 google.com
ip a
ip route
```

인터넷 연결 및 DNS 동작 여부를 점검하였다.

---

## Cause Analysis

추가 테스트 결과 Jetson 장비 자체의 네트워크 문제는 아니었다.

다음 환경에서는 정상적으로 인터넷 연결이 가능하였다.

* Wi-Fi 공유기 LAN 포트
* 스마트폰 USB 테더링

반면 학교 건물 내 벽면 LAN 포트에서는 인터넷 연결이 불가능하였다.

이를 통해 Jetson 설정 문제가 아닌 학내 네트워크 정책 또는 인증 절차에 의한 제한으로 판단하였다.

예상 원인:

* 기기 등록(MAC Address Registration)
* NAC(Network Access Control)
* 사용자 인증 절차
* 학내 네트워크 정책

---

## Temporary Solution

개발 환경 구축을 위해 스마트폰 USB 테더링을 사용하였다.

### Procedure

1. 스마트폰 USB 연결
2. USB 테더링 활성화
3. Jetson에서 네트워크 장치 자동 인식 확인

---

## Result

USB 테더링을 이용하여 정상적으로 인터넷 연결에 성공하였다.

이를 통해 다음 작업을 수행하였다.

* apt update
* apt install
* Git Clone
* Python Package 설치
* CUDA 관련 패키지 설치
* 개발 환경 구성

---

# Post Installation Configuration

## 1. USB Webcam Recognition Test

Logitech C922 USB Webcam 연결 후 장치 인식 여부를 확인하였다.

```bash
ls /dev/video*
```

실행 결과:

```text
/dev/video0
/dev/video1
```

USB Webcam이 정상적으로 등록된 것을 확인하였다.

---

## 2. V4L2 Device Check

장치 정보를 확인하기 위해 다음 명령을 사용하였다.

```bash
v4l2-ctl --list-devices
```

이를 통해 Logitech Webcam이 정상적으로 인식된 것을 확인하였다.

---

## 3. Camera Validation

카메라 동작 여부를 확인하기 위해 OpenCV 기반 테스트를 수행하였다.

주 사용 장치:

/dev/video0

실시간 영상 입력이 정상적으로 동작하는 것을 확인하였다.

---

## 4. Package Manager Issue

패키지 설치 과정에서 apt Cache Lock 문제가 발생하였다.

대표적인 증상:

Waiting for cache lock

Could not get lock

원인 분석 결과 다른 프로세스가 apt 패키지 관리자를 사용 중인 상태였다.

해결 과정:

```bash
ps aux | grep apt
sudo dpkg --configure -a
sudo apt update
```

---

## 5. Korean Language Environment

Jetson Ubuntu 환경에서 한글 입력 환경 구성을 시도하였다.

설정 항목:

* Korean Language Pack
* IBus
* ibus-hangul

설치 명령:

```bash
sudo apt install ibus-hangul
```

### Result

한글 입력 환경 구성을 시도하였으나 정상 동작하지 않았다.

### Future Work

* IBus 설정 재검토
* 입력기 환경 추가 검증
* Jetson Ubuntu 환경 호환성 확인

---

# Final Result

최종적으로 다음 개발 환경 구축을 완료하였다.

* Ubuntu Desktop
* JetPack
* CUDA
* Python Development Environment
* USB Webcam
* OpenCV Environment

이를 기반으로 이후 Depth Anything V2 및 V3 개발 환경 구축을 진행하였다.

---

# Lessons Learned

## Development Environment

* Windows 환경에서도 WSL2를 이용하여 Jetson 개발 환경을 구축할 수 있다.
* BIOS 가상화 설정은 WSL2 사용을 위한 필수 조건이다.
* SDK Manager 사용 시 WSL 환경 검증이 중요하다.

## Flashing

* Jetson 플래싱 과정에서는 안정적인 전원 공급이 중요하다.
* 플래싱 도중 오류가 발생하더라도 Ubuntu가 부분적으로 설치될 수 있다.
* JetPack 설치 완료 여부는 실제 개발 환경 검증을 통해 확인해야 한다.

## Networking

* Jetson 자체 네트워크 문제와 네트워크 인프라 문제를 구분하는 것이 중요하다.
* 학내 벽면 LAN 포트는 추가 인증 또는 등록 절차가 필요할 수 있다.
* 동일 장비를 다른 네트워크 환경에서 테스트하면 원인 분석에 도움이 된다.
* USB 테더링은 초기 개발 환경 구축 시 유용한 대체 수단이 될 수 있다.

## Development

* 실제 카메라 및 CUDA 테스트를 통해 개발 환경을 검증해야 한다.
* 초기 환경 구축 과정에서 발생한 문제와 해결 방법을 기록해두는 것이 이후 유지보수에 도움이 된다.
