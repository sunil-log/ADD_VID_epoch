
src 안의 파일 설명

# 01_preprocessing.py
1. **Linear Detrend 및 Band-Pass Filter 적용:** 
   EEG 데이터에 linear detrend를 적용하여 추세를 제거하고, 지정된 하한(low_Hz)과 상한(high_Hz) 사이의 주파수를 가진 신호만을 통과시키는 band-pass filter를 적용합니다.

2. **Average Reference 적용:**
   EEG 데이터의 모든 채널에 대해 평균 참조를 적용합니다. 이는 데이터를 더 깨끗하게 만드는 데 도움이 됩니다.

3. **Event 기반 데이터 자르기 및 연결:**
   특정 이벤트를 기반으로 EEG 데이터의 앞뒤를 잘라내고, 각 15초 길이의 부분들을 이어 붙여 동영상 시청 중의 데이터만을 추출합니다.

4. **특정 채널 추출:**
   E1부터 E64까지의 채널과 VREF 채널만을 추출하며, STRT, stim, STI 014와 같은 다른 채널들은 제거합니다.

5. **결과물 저장:**
   처리된 데이터를 fif 파일 형식으로 `target_dir`에 저장합니다.

## 입력 매개변수
- `raw_dir`: 원본 mff 파일이 위치한 디렉토리
- `target_dir`: 처리된 데이터를 저장할 디렉토리
- `low_Hz`: band-pass filter의 하한 주파수
- `high_Hz`: band-pass filter의 상한 주파수