# ⚠️ 주의: 읽기 전용 폴더 (Read-Only)  
이 디렉토리는 @yeramonster의 개인 리포지토리와 **자동 동기화**되고 있습니다.  
공동 리포지토리에서 직접 수정할 경우, 동기화 과정에서 내용이 삭제되거나 꼬일 수 있으니  
수정이 필요하시면 반드시 관리자에게 문의해 주세요.  

# rainbow_robotics_rb5-850_manual  
한팔로봇 프로그래밍을 위한 기초적인 예제
> * rbpodo_ex.py 는 rbpodo 깃허브의 예제와 동일함  
> * 티치팬던트 가장 오른쪽 상단에 보이는 두 좌표 중  
왼쪽 좌표는 move_l로 사용되는 좌표이고,  
오른쪽 좌표는 move_j로 사용되는 좌표이다. 
  * move j - 각 관절 각도를 지정합니다. 6개의 관절이 동시에 움직이는 특징이 있습니다. 
  * move l - X, Y, Z 축 위치값 및 A, B, C 축 회전 각도를 설정합니다. A, B, C -> rx, ry, rz

# 링크  
> :: rbpodo github  
> https://github.com/RainbowRobotics  
> https://github.com/RainbowRobotics/rbpodo  
>
> :: from rainbow import cobot 사용 가능. (rb_pose_test 파일)  
> https://pypi.org/project/rb-api-python/  

# 로봇 IP
* ROBOT_IP = "172.16.3.128" #308호 로봇암 현재 주소  

# 코드 파일 설명
> * [rb_ex1.py] : 실시간 위치 전송  
> * [rb_ex2.py] : move_l 
              ; 로봇암 기존 좌표에서 target_point = np.array([x, y, z, rx, ry, rz]) 에 위치 좌표값을 입력된 값만큼 +로 이동.  
> * [rb_ex3.py] : move_j 
              ; joint = np.array([base, shoulder, elbow, wrist1, wrist2, wrist3]) 에 입력된 joint 값으로 이동.
> * [codot_pose_head] : [cobot_pode_test] 에 사용되는 cobot 라이브러리 불러온 파일  
> * [cobot_pose_test] : 코드 내에서 지정한 5개의 pose(1~5)를 반복 동작함. 이때, 사용되는 좌표는 move_l에 사용되는 값과 동일함.


