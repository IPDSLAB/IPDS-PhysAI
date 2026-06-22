# Jetson Orin NX Setup

## Objective

Jetson Orin NX 환경에서 AI 비전 모델을 실행하기 위한 개발 환경을 구축한다.

## Hardware

* Jetson Orin NX 16GB
* Host PC : Windows Laptop
* Logitech C922 Webcam

## Software

* JetPack 6.2
* Ubuntu 22.04
* CUDA 12.6
* Python 3.10

## Procedure

### 1. SDK Manager 설치

Windows 환경에서 NVIDIA SDK Manager를 설치하였다.

### 2. Jetson Recovery Mode 진입

Jetson Orin NX를 Recovery Mode로 진입시킨 후 USB로 Host PC와 연결하였다.

### 3. JetPack 설치

SDK Manager를 이용하여 Ubuntu 및 JetPack 6.2를 설치하였다.

### 4. Ubuntu 초기 설정

사용자 계정 생성 및 기본 네트워크 설정을 진행하였다.

### 5. CUDA 환경 확인

CUDA Toolkit 설치 여부를 확인하고 GPU 동작을 검증하였다.

## Issues

### USB Device Recognition

SDK Manager에서 Jetson 장치를 인식하지 못하는 문제가 발생하였다.

### Solution

Recovery Mode 재진입 및 USB 연결 상태를 재확인하여 해결하였다.

## Result

Jetson Orin NX 개발 환경 구축 완료.
