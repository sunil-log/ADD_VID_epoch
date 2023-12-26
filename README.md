

# 01_preprocessing.py
Band-Pass Filter 적용 및 동영상 시청부분 추출

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


# 02_average_all_subjects.py
각 event epoch 의 평균 시각화 (optional)

1. **모든 피험자 데이터 평균화:**
   모든 피험자의 EEG 데이터에 대해 평균을 내어 전체적인 경향성을 파악합니다.

2. **이벤트 파일 읽기 및 특정 이벤트 평균화:**
   'answer_sheet.npy'라는 이벤트 파일을 읽어들여, 특정 이벤트(예: 군인, 멧돼지, 없음)에 대한 EEG 데이터만을 추출하여 이들의 평균을 계산합니다.

이러한 과정을 통해 특정 이벤트에 대한 뇌파 반응의 평균적인 양상을 확인할 수 있으며, 이를 통해 각각의 이벤트가 피험자의 뇌파에 어떠한 영향을 미치는지 분석할 수 있습니다.
