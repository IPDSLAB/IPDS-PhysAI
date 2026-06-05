iveview · PY
"""
카메라 라이브뷰 (Canon EOS R8)
gphoto2 영상 → ffplay 로 미리보기
종료: ffplay 창에서 Q 또는 터미널에서 Ctrl+C
"""
import subprocess
import shutil
import time
 
def start_liveview():
    # 0) 사전 점검: ffplay / gphoto2 설치 확인
    for tool in ("gphoto2", "ffplay"):
        if shutil.which(tool) is None:
            print(f"❌ '{tool}' 가 설치되어 있지 않습니다.")
            if tool == "ffplay":
                print("   → sudo apt install ffmpeg")
            return
 
    # 1) gvfs 가 카메라를 점유 중이면 해제
    subprocess.run("pkill -f gvfsd-gphoto2", shell=True)
    time.sleep(0.5)
 
    print("라이브 뷰 시작... (종료: 창에서 Q 또는 Ctrl+C)")
    cmd = ("gphoto2 --capture-movie --stdout | "
           "ffplay -i - -window_title 'EOS R8 Preview' -loglevel quiet")
 
    # 2) 프로세스 그룹으로 실행 (자식까지 한 번에 종료하기 위함)
    process = None
    try:
        process = subprocess.Popen(cmd, shell=True, start_new_session=True)
        process.wait()
    except KeyboardInterrupt:
        print("\n사용자에 의해 종료됨")
    finally:
        # 3) gphoto2 / ffplay 잔여 프로세스 정리
        if process is not None:
            process.terminate()
        subprocess.run("pkill -f capture-movie", shell=True)
        subprocess.run("pkill -f ffplay", shell=True)
        print("정리 완료")
 
if __name__ == "__main__":
    start_liveview()
 
