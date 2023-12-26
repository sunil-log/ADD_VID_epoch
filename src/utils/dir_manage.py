import os
import shutil

def recreate_directory(dir_path):
	"""
	주어진 디렉터리가 존재할 경우, 내부의 모든 파일을 삭제하고 해당 디렉터리를 제거한 후, 다시 생성합니다.

	:param dir_path: 재생성할 디렉터리의 경로
	"""

	# 디렉터리가 존재하는 경우, 내부 파일을 삭제하고 디렉터리를 제거
	if os.path.exists(dir_path):
		shutil.rmtree(dir_path)

	# 디렉터리를 다시 생성
	os.makedirs(dir_path)
