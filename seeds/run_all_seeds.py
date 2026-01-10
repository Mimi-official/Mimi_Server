import sys
import os

# [핵심 수정 사항]
# 현재 파일(run_all_seeds.py)의 부모 폴더(프로젝트 루트)를 파이썬 경로에 강제로 추가합니다.
# 이렇게 해야 'from app import create_app'이 작동합니다.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 이제 import가 정상적으로 작동합니다
from seed_wonbin import seed_wonbin
from seed_jiyeon import seed_jiyeon
from seed_minjae import seed_minjae
from seed_seohyun import seed_seohyun
from seed_jungwon import seed_jungwon
from seed_seowoo import seed_seowoo

print("============== 데이터 초기화 시작 ==============")

# 순서대로 실행 (이 순서가 ID가 됩니다)
print("[1/6] 조원빈 데이터 생성 중...")
seed_wonbin()

print("[2/6] 한지연 데이터 생성 중...")
seed_jiyeon()

print("[3/6] 김민재 데이터 생성 중...")
seed_minjae()

print("[4/6] 강서현 데이터 생성 중...")
seed_seohyun()

print("[5/6] 민정원 데이터 생성 중...")
seed_jungwon()

print("[6/6] 윤서우 데이터 생성 중...")
seed_seowoo()

print("============== 모든 데이터 생성 완료! ==============")