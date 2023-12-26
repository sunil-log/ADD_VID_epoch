

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

# 03_epochs_sliding_window.py
Sliding Window를 통한 epoch data $X$ 및 label $y$ 생성

1. **Numpy 배열로 데이터 로드:**
   각 피험자의 fif 파일을 numpy 배열로 변환합니다.

2. **시간축에 따른 Epoch 추출:**
   정의된 `sliding_window_size_sec` 크기의 window를 사용하여 시간축을 따라서 연속적인 데이터 블록(epoch)을 추출합니다.

3. **Window 이동 및 이벤트 라벨링:**
   `sliding_window_stride_sec` 만큼 window를 이동시키면서, window 안에 특정 이벤트(예: 군인, 멧돼지)가 존재하는 경우 해당 이벤트에 대한 라벨(0: no event, 1: 군인, 2: 멧돼지)을 저장합니다.

4. **Epoch 및 라벨 저장:**
   추출된 epoch과 해당 라벨을 npz 파일 형태로 저장합니다. 이 파일은 데이터(X)와 라벨(y)을 포함합니다.

## 입력 매개변수
- `dir_fif`: raw fif 파일이 저장된 디렉토리
- `sample_Hz`: EEG 데이터의 샘플링 비율
- `events_npy`: 동영상의 이벤트 정보가 담긴 npy 파일
- `w_size_sec`: sliding window의 크기(초)
- `w_stride_sec`: sliding window의 stride(초)
- `scale_factor`: EEG 전압에 적용할 스케일링 인자 (e.g. fif 를 npy로 변경시 단위는 V 이므로 1e6을 곱해 uV로 변경)