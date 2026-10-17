# 합성 marker 탐색 분석 실행 기록

입력: context.md, metadata.tsv, measurements.tsv. 출력 단위: 이미 정규화된 log2 intensity.
관심 효과: 서로 다른 독립 기증자의 treated-control 평균 차이; control 및 batch A가 기준.
추가 로그 변환, 반올림, 정규화, 대체, 표본·marker 제외 없음. 0은 척도상의 값이며 NA만 결측.
원본 보존. 실행 경로: 스크립트가 있는 디렉터리. 확률적 연산 없음.

환경: Python 3.12.7, NumPy 2.1.3, pandas 2.3.1, SciPy 1.16.0, statsmodels 0.14.5.

## 입력 식별과 연결

- context.md: SHA256 0e3d1de28a15706052a1c16f80ffe9bd7d63da8cd3c28f08af4e053d8ab59ace
- metadata.tsv: SHA256 8f22cab0aebd78567a12f1eca66d75cbfc2a2007ab6e19f2ae69bd21a47d863e
- measurements.tsv: SHA256 01ff3f8d1bb8c6018b7d166434e00570ee3c0e202a5d89b69f25fd0cd8518d93

전후 표본 8→8, marker 3→3; 독립 donor 8; 결측 0; 0 값 0; 범위 4.800–9.200.
측정 열의 원래 순서는 metadata와 다름. sample_id로 연결한 모든 관측:
```text
          donor_id condition batch  marker_A  marker_B  marker_C
sample_id                                                       
S01            D01   control     A       7.0       5.0       9.0
S02            D02   control     B       7.2       5.2       9.2
S03            D03   control     A       6.8       4.8       8.8
S04            D04   control     B       7.1       5.1       9.1
S05            D05   treated     A       8.0       5.1       8.9
S06            D06   treated     B       8.1       5.3       9.1
S07            D07   treated     A       7.9       4.9       8.7
S08            D08   treated     B       8.2       5.2       9.0
```
## 조건·배치와 독립 반복

```text
batch      A  B
condition      
control    2  2
treated    2  2
```
설계 행렬 [intercept, treated, batch_B] rank=3/3; 잔차 자유도 5. 각 조건 독립 donor n=4, 기술 반복 없음.

## 조건별 분포 (log2 intensity)

```text
                      count   mean     std  median  min  max
feature_id condition                                        
marker_A   control        4  7.025  0.1708    7.05  6.8  7.2
           treated        4  8.050  0.1291    8.05  7.9  8.2
marker_B   control        4  5.025  0.1708    5.05  4.8  5.2
           treated        4  5.125  0.1708    5.15  4.9  5.3
marker_C   control        4  9.025  0.1708    9.05  8.8  9.2
           treated        4  8.925  0.1708    8.95  8.7  9.1
```
## QC 확인 뒤 추가 실행: 배치 보정 및 기증자 영향 점검

모형: intensity ~ intercept + treated + batch_B, 독립 기증자 단위 OLS. 관측값은 그대로 사용하며 paired 분석은 하지 않음. 배치별 수준 차이 때문에 배치를 보정함. 관심값은 동일 배치에서의 treated-control 차이를 공통 효과로 요약한 계수.

```text
            raw_difference  batch_adjusted_difference  ci95_low  ci95_high  batch_B_minus_A  residual_sd
feature_id                                                                                              
marker_A             1.025                      1.025    0.8702     1.1798            0.225       0.0851
marker_B             0.100                      0.100   -0.0818     0.2818            0.250       0.1000
marker_C            -0.100                     -0.100   -0.2818     0.0818            0.250       0.1000
```
95% 구간은 잔차의 독립성·정규성·등분산성과 가법 모형에 의존하는 t 구간(df=5). 각 marker별 구간이며 3개 전체에 대한 동시 구간이 아님. 탐색 요약으로 p값 검정·유의성 판정은 하지 않음.

```text
            within_batch_A_difference  within_batch_B_difference  leave_one_donor_out_min  leave_one_donor_out_max
feature_id                                                                                                        
marker_A                         1.05                        1.0                     0.98                     1.06
marker_B                         0.10                        0.1                     0.06                     0.14
marker_C                        -0.10                       -0.1                    -0.14                    -0.06
```
배치 내 비교는 조건별 n=2. leave-one-donor-out은 매번 1명을 제외해 다시 적합한 효과의 범위이며 신뢰구간이 아님. 본 분석은 8명 전원 유지.

## 관측의 해석과 다음 판단

- marker_A: treated-control +1.025 log2 단위, 95% 구간 [0.870, 1.180]. 모형의 가정 아래 방향이 비교적 분명한 패턴이며 실제 생물학적 검증은 아님.
- marker_B: treated-control +0.100 log2 단위, 95% 구간 [-0.082, 0.282]. 구간에 0이 포함되며 효과 없음·동등성의 근거로 해석하지 않음.
- marker_C: treated-control -0.100 log2 단위, 95% 구간 [-0.282, 0.082]. 구간에 0이 포함되며 효과 없음·동등성의 근거로 해석하지 않음.

현재 균형 설계에서는 보정 전후 조건 계수가 같음. 이는 배치 차이가 없다는 뜻이 아니며 batch B의 수준은 A보다 marker별 0.225–0.250 높음.
현재 자료에 필요한 추가 점검인 배치별 대비와 기증자 한 명씩 제외한 민감도 분석을 실행했고, 모든 marker의 차이 방향이 유지됨. 독립 검증이나 제외 근거로 사용하지 않음.
실제 연구로 이어갈 경우 처리 배정·실험 기록을 확인하고 조건×배치를 균형 있게 구성한 추가 독립 기증자로 작은 효과의 정밀도와 재현성을 확인해야 함. 현재 합성 자료만으로 이를 추가 검증할 수 없음.

## 실행과 범위

초기 QC 실행: `python analysis.py` (효과 분석 구현 전에 출력 확인). 그 결과 배치 내 대비와 기증자 영향 점검을 사후 탐색으로 추가함.
최종 재실행: `python analysis.py > analysis_record.md`. 같은 디렉터리에 `results.tsv`와 이 기록을 생성함. 원본과 비교 방향은 변경하지 않음.
그림 없이 전 관측과 분포·효과 표로 확인. 외부 annotation, 문헌 검색, 패키지 설치, 실제 생물학적 검증은 수행하지 않음.
8명뿐이므로 잔차 분포·등분산성과 조건×배치 상호작용을 충분히 검증할 수 없음. 반복 수가 적어 작은 효과의 정밀도가 제한됨. 처리 무작위 배정 여부는 제공되지 않았으며 인과 효과로 해석하지 않음. 합성 자료의 수치 패턴이므로 실제 사람 세포의 생물학적 효과·기전·marker 기능을 주장할 수 없음.
