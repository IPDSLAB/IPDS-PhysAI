# Depth Anything V3

## Objective

Jetson Orin NX 환경에서 Depth Anything V3를 설치하고 실시간 추론 환경을 구축한다.

## Environment

* Jetson Orin NX 16GB
* CUDA 12.6
* Python 3.10
* Logitech C922 Webcam

## Installation

Depth Anything V3 저장소를 설치하고 의존성 라이브러리를 구성하였다.

## Issues

### NumPy Version Conflict

OpenCV와 NumPy 버전 충돌이 발생하였다.

### Solution

NumPy 1.26.4 버전으로 변경하여 해결하였다.

### xFormers Build

Jetson 환경에서 xFormers 설치 과정이 필요하였다.

### pycolmap Warning

pycolmap 관련 경고가 발생하였으나 실시간 Depth 추론에는 영향을 주지 않았다.

## Real-Time Webcam Test

Logitech C922 웹캠을 연결하여 실시간 Depth Estimation을 수행하였다.

## Optimization

실시간 추론 성능 향상을 위해 다음 항목을 조정하였다.

* Input Resolution
* Processing Resolution
* Inference Interval

## Result

실시간 Webcam 기반 Depth Estimation 데모를 성공적으로 수행하였다.

## Conclusion

Jetson Orin NX에서 Depth Anything V3의 실시간 실행 가능성을 검증하였다.
