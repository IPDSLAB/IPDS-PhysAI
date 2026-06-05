"""
TCP 포즈 확인 스크립트
━━━━━━━━━━━━━━━━━━━━━
로봇 엔드포인트의 현재 TCP 포즈가 올바르게 읽히는지 확인
sdata 전체 속성 목록도 함께 출력해서 정확한 속성명 파악
"""
 
import asyncio
import rbpodo as rb
import numpy as np
 
ROBOT_IP = "172.16.3.128"
 
async def check_tcp_pose():
    print("=" * 55)
    print("  TCP 포즈 확인")
    print("=" * 55)
 
    data_channel = rb.asyncio.CobotData(ROBOT_IP)
 
    # ── 1회: sdata 전체 속성 출력 ─────────────────────────────
    data = await data_channel.request_data()
 
    print("\n[sdata 전체 속성 목록]")
    attrs = [a for a in dir(data.sdata) if not a.startswith("_")]
    for a in attrs:
        try:
            val = getattr(data.sdata, a)
            print(f"  {a:30s} = {val}")
        except Exception as e:
            print(f"  {a:30s} = (읽기 오류: {e})")
 
    # ── TCP 포즈 후보 속성명 시도 ─────────────────────────────
    print("\n[TCP 포즈 후보 속성 시도]")
    candidates = [
        "tcp_ref",
        "task_pos",
        "tcp_pos",
        "tcp",
        "task_ref",
        "fkin",
        "p_ref",
    ]
    found_attr = None
    for attr in candidates:
        try:
            val = getattr(data.sdata, attr)
            print(f"  ✅ {attr} = {val}")
            found_attr = attr
        except AttributeError:
            print(f"  ❌ {attr} → 없음")
 
    # ── 찾은 속성으로 실시간 출력 (5회) ──────────────────────
    if found_attr:
        print(f"\n['{found_attr}' 실시간 출력 - 5회]")
        print(f"  {'X':>10} {'Y':>10} {'Z':>10} {'RX':>10} {'RY':>10} {'RZ':>10}  (mm / deg)")
        print("  " + "-" * 68)
        for i in range(5):
            data = await data_channel.request_data()
            pose = np.array(getattr(data.sdata, found_attr))
            print(f"  {pose[0]:10.3f} {pose[1]:10.3f} {pose[2]:10.3f}"
                  f" {pose[3]:10.3f} {pose[4]:10.3f} {pose[5]:10.3f}")
            await asyncio.sleep(0.5)
        print("\n  ✅ TCP 포즈 확인 성공!")
        print(f"  step2_collect_data.py 35번째 줄을 다음으로 수정:")
        print(f"  g.tcp_pose = np.array(data.sdata.{found_attr})")
    else:
        print("\n  ⚠️  위 속성 목록에서 TCP 포즈에 해당하는 항목을 직접 확인하세요")
 
    print("=" * 55)
 
if __name__ == "__main__":
    asyncio.run(check_tcp_pose())
