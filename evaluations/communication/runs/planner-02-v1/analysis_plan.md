# 배치를 고려한 처리 비교 분석 계획

작성일: 2026-10-21. 범위: 설계와 가벼운 입력 점검만 수행했다. 입력 수치 전체를 이미 읽었으므로 사전등록 계획이 아니다.

## 판단과 연구 질문

현재 자료로 **배치와 분리된 처리 효과는 추정할 수 없다.** control은 전부 A, treated는 전부 B에 속해 처리 지표와 배치 지표가 같다. 권장 출발점은 각 donor의 측정값과 **treated/B − control/A의 관찰된 차이**를 기술하는 것이다. 이는 처리, 배치 및 집단 간 donor 차이가 섞인 비교이며 처리 효과의 검정으로 해석하지 않는다. 배치 보정 알고리즘을 바꾸어도 비어 있는 조합의 관측 정보는 생기지 않는다.

원래 질문은 동일 배양 조건에서 24시간 처리한 사람 유래 배양 세포의 marker 측정값이 control보다 얼마나 변하는지다. 비교 방향은 treated − control, 결과 단위는 정규화된 log2 intensity이다. 독립 단위는 donor이며 현재는 군별 3명이다. 같은 donor의 전후 비교는 아니다. 이 자료는 합성·가상 marker 예제이므로 실제 사람의 생물학적 효과나 기전으로 일반화할 수 없다. 이번 설계의 결정은 현재 파일로 설명 가능한 범위를 정하고, 처리 효과를 구분하려면 어떤 기록 또는 관측이 필요한지 밝히는 것이다.

## 실제 확인한 근거

`context.md`, `metadata.tsv`, `measurements.tsv` 전체를 읽었다. Python 3.12.7 표준 라이브러리로 아래 점검만 실행했다.

| 근거 구분 | 확인한 내용과 출처 | 설계에 미치는 영향 |
| --- | --- | --- |
| 제공 기록 | context: 합성 bulk marker, 정규화된 log2 intensity, 독립 donor 6명, 각 1회, 동일 배양 조건의 24시간 처리 비교 | 원시 count 모델, 정수화, 재로그 변환을 적용하지 않는다. 실제 독립성은 실험 기록에 근거한 설명이며 파일만으로 생물학적으로 검증한 것은 아니다. |
| 전체 입력 점검 | 2 marker × 6 sample, metadata 6행, 고유 donor 6명. sample/feature 중복과 반복 donor 없음. 두 파일 sample ID가 모두 일치하고 순서도 동일 | 현 자료에서는 군별 독립 donor n=3인 비짝지은 관측이다. 결합은 ID로 수행한다. donor 고정효과를 추가할 반복 관측이 없다. |
| 전체 입력 점검 | metadata 빈 필드 0, 측정값 12개 모두 유한수, 결측·0 값 0. 전체 범위 4.8–8.7 log2 intensity | 결측 대치나 0 처리 불필요. 이 확인만으로 정규화의 적절성이나 생물학적 타당성이 입증되지는 않는다. |
| 설계 점검 | 아래 교차표 및 처리/배치 지표 열의 완전 일치 | 처리와 배치의 개별 계수를 식별하지 못한다. 군마다 배치는 하나여서 배치 간 변동을 반복 관측한 것도 아니다. |
| 잠정 가정 | 기록에 제시된 log2 intensity가 모든 sample에서 비교 가능한 공통 척도 | 기술 비교를 계획할 수 있으나 생성·정규화 기록으로 확인해야 한다. 군별 서로 다른 기준으로 정규화했다면 집단 간 수치 차이 해석을 보류한다. |

| condition | 배치 A: 독립 donor 수 | 배치 B: 독립 donor 수 |
| --- | ---: | ---: |
| control | 3 | 0 |
| treated | 0 | 3 |

설계행렬 `[절편, treated 지표, batch B 지표]`의 서로 다른 행은 `[1,0,0]`, `[1,1,1]`뿐이다. 마지막 두 열이 같고 절편과 처리 지표는 독립이므로 열 3개에 rank 2이다. 이는 입력 구조에 대한 대수적 확인이며 결과 모형을 적합한 것이 아니다.

## 권장 순서와 판단 분기

| 질문과 목적 | 최소 방법 및 필요한 입력 | 검토할 산출물 | 결과에 따른 결정 |
| --- | --- | --- | --- |
| 현재 집단에서 어떤 차이가 관찰되는가? | 공통 척도를 잠정 전제로 현재 두 TSV에서 donor별 값을 연결하고, marker별 군 평균·범위와 treated/B − control/A 평균 차이를 계산한다. | donor 3개씩을 모두 표시한 점도표와 n·평균·범위·차이 표. 축은 log2 intensity, 집단 표기는 condition와 batch를 함께 쓴다. | 값이 분리되어 보여도 처리/배치 원인을 구분하지 못한다. 겹치거나 donor별 산포가 크면 차이가 명확하지 않다고 기술하며, 차이가 작아도 처리 효과가 없다고 결론 내리지 않는다. 한 점의 영향이 크면 기록 확인 대상으로 남기고 유의성을 위해 제외하지 않는다. |
| 측정척도와 배치의 의미가 비교를 허용하는가? | 생성·정규화 방법, 배치가 배양일/처리일/추출/측정 run 중 무엇인지, 선행 보정 여부를 기록에서 확인한다. 제공 파일에는 이 정보가 없다. | sample별 배치 정의·처리 배정·전처리 기록을 연결한 표 | 공통 기준이면 위 기술 비교를 유지한다. 서로 다른 기준이면 재처리 가능한 입력과 공통 기준부터 확보한다. 기록이 불명확하면 비교는 잠정 수치 요약에 머문다. |
| 배치와 구분되는 처리 대비를 새로 확보할 수 있는가? | 배치 안에 control과 treated가 함께 있는 실험 기록 또는 추가 관측을 확보하고 교차표·독립 donor 수·설계 rank를 재점검한다. | 조건×배치별 독립 donor 수와 배정/반복 관계 표 | 완전 교락이 유지되면 처리 추론을 중단한다. 교차 관측이 확보되면 추론 설계를 갱신한다. 조합은 채웠지만 donor 수가 적거나 겹침이 제한되면 모형이 계산되어도 불확실성이 클 수 있으므로 탐색적 범위와 추가 반복 필요성을 명시한다. |

현재 기술 요약에는 처리 효과의 p값이나 다중검정을 붙이지 않는다. 군 내 범위는 관찰된 donor 변동을 보여줄 뿐 배치 효과나 처리 효과의 신뢰구간이 아니다. marker는 가상 명칭뿐이므로 경로 분석이나 기전 주장을 계획하지 않는다.

교차 관측 확보 후에만, 공통 척도와 독립성이 확인된 donor별 값에 대해 `log2 intensity ~ condition + batch` 같은 가산 모형을 후보로 검토한다. 처리 계수는 treated − control이며, 가산성·잔차·배치별 대비의 일관성을 점검할 수 있는 반복이 필요하다. donor 내 두 조건을 새로 측정한다면 짝 관계를 보존하는 설계로 바꾼다. 두 marker를 모두 검정하기로 정할 경우 같은 두 검정을 하나의 다중검정 집합으로 사전에 정의하고, 추정 차이와 donor 구조를 반영한 불확실성을 함께 보고한다. 중요하다고 볼 변화 크기는 실험 목적·측정 정밀도 정보로 정하며 현재 수치에서 임의로 정하지 않는다. 무작위 배정과 관련 교란요인 기록이 없는 한 인과적 처리 효과로 확대하지 않는다.

## 필요한 정보와 추가 관측

| 미확인 항목 | 답에 따라 바뀌는 선택 |
| --- | --- |
| 처리 물질·용량, 세포 종류, donor 모집/배정 기준 및 무작위화 여부 | 결과가 적용되는 대상과 인과적 해석의 범위를 정한다. 현재 기록으로 구체적 표적이나 효과 크기를 설정하지 않는다. |
| 배치 정의·일자·장비/실험자, 측정 생성 방법 및 정규화 기준 | 기술적 run 차이와 배양/처리 조건 차이를 구분하고 공통 척도를 확인한다. |
| 기존에 누락된 교차 관측 또는 보관 시료 존재 여부 | 실제 A-treated, B-control 관측이 있다면 독립 단위와 QC를 확인해 설계를 다시 점검한다. 없다면 새로 수집할 설계를 정한다. |

추가 실험에서는 여러 독립 배치 각각에 두 조건을 함께 배치하고, 각 조건에 독립 donor 반복을 확보하는 것을 우선한다. 가능하다면 donor의 세포를 두 조건에 나누어 배정하고 배치 내 처리 순서를 균형화하되, 실제 가능 여부와 생물학적 목표를 먼저 확인한다. 같은 시료를 다른 run에서 다시 측정하는 것은 기술적 연결 정보이며 독립 donor 수를 늘리지 않는다. 새 날짜의 측정을 기존 배치 A/B의 관측으로 임의 간주해서도 안 된다. 필요한 표본 수나 검정력은 현재의 완전 교락 자료만으로 보장하지 않는다.

## 다음 실행 가능한 단계와 완료 기준

이미 끝낸 ID·결측·교차표 점검을 다음 할 일로 반복하지 않는다. **후속 분석에서 바로 실행할 첫 단계**는 현재 `metadata.tsv`와 `measurements.tsv`를 sample ID로 연결해 donor별 표를 만들고, marker별 `n, mean, min, max, treated/B − control/A`를 출력하는 것이다. marker별 점도표에는 6개 관측을 모두 표시한다. 입력은 이 계획과 같은 디렉터리의 두 TSV이며, 입력 값을 재변환하지 않는다. 판정 기준은 차이의 유의성이 아니라 표와 그림이 배치가 결합된 두 집단의 관찰값을 정확히 보여주는지다. 비교척도 기록이 이를 부정하면 군별 요약만 남기고 집단 간 차이의 해석을 보류한다.

처리 효과 모형으로 넘어가기 위한 미해결 첫 단계는 위의 배치·정규화·배정 기록과 교차 관측 유무를 확인하는 것이다. 필요한 정보는 제공 자료에 없으므로 현재 실행 가능한 기술 요약과 병행할 수 있으나, 정보 없이 처리 계수를 적합하지 않는다.

후속 기술 분석의 완료 산출물은 donor별 표, 두 marker의 요약표와 점도표, 비교 단위와 교락 한계를 명시한 해석, 재실행 코드이다. 이번 요청은 설계까지이므로 이 요약 계산·그림·모형·검정은 **실행하지 않았다**. 현재 준비된 것은 기술 분석의 시작이며, 배치와 분리된 처리 추론은 준비되지 않았다.

## 재현 기록

작업 디렉터리는 `/tmp/bio-comm-20261021-planner`이다. 외부 자료·문헌은 조회하지 않았으며, 제공 기록과 실제 설계의 열 일치에 근거했다. 아래는 실제 실행한 전체 입력 점검 코드이며 모형 적합은 포함하지 않는다.

```python
import csv, hashlib, json, math, sys
from collections import Counter
from pathlib import Path

root = Path(".")
metadata = list(csv.DictReader((root / "metadata.tsv").open(), delimiter="\t"))
with (root / "measurements.tsv").open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    columns = reader.fieldnames
    matrix = list(reader)
samples = columns[1:]
ids = [row["sample_id"] for row in metadata]
donors = [row["donor_id"] for row in metadata]
features = [row["feature_id"] for row in matrix]
raw = [row[sample] for row in matrix for sample in samples]
values = [float(value) for value in raw if value not in ("", "NA", "NaN")]
design = [(1, int(row["condition"] == "treated"), int(row["batch"] == "B"))
          for row in metadata]
summary = {
    "python": sys.version.split()[0],
    "metadata_rows": len(metadata),
    "unique_donors": len(set(donors)),
    "duplicate_sample_ids": [key for key, n in Counter(ids).items() if n > 1],
    "repeated_donors": [key for key, n in Counter(donors).items() if n > 1],
    "duplicate_measurement_columns": [key for key, n in Counter(samples).items() if n > 1],
    "duplicate_feature_ids": [key for key, n in Counter(features).items() if n > 1],
    "measurement_shape": [len(matrix), len(samples)],
    "metadata_only_samples": sorted(set(ids) - set(samples)),
    "matrix_only_samples": sorted(set(samples) - set(ids)),
    "same_sample_order": ids == samples,
    "missing_metadata_fields": sum(value in ("", None) for row in metadata for value in row.values()),
    "missing_values": len(raw) - len(values),
    "nonfinite_values": sum(not math.isfinite(value) for value in values),
    "zero_values": sum(value == 0 for value in values),
    "value_range_log2_intensity": [min(values), max(values)],
    "condition_by_batch": {condition: {batch: sum(row["condition"] == condition and row["batch"] == batch for row in metadata) for batch in ("A", "B")} for condition in ("control", "treated")},
    "design_unique_rows_intercept_treated_batchB": sorted(set(design)),
    "treated_and_batchB_columns_identical": all(row[1] == row[2] for row in design),
    "sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
               for name in ("TASK.md", "context.md", "metadata.tsv", "measurements.tsv")}
}
print(json.dumps(summary, ensure_ascii=False, indent=2))
```

점검 출력의 핵심 수치는 위 표에 기록했다. 실행 시 입력 SHA-256은 다음과 같다.

```text
TASK.md          7ac0a21c29814e549bc3c2867e30c70008852be4d840cc32b69a4cfee0293c83
context.md       540bce3b2ba0f37c8bab222e640e21d98098c70d7a6469ea887dcda58d20f4e4
metadata.tsv     a3e6dd70a4f26218d386f7b909505eb22be0da922a1b53a942c1123698a0014f
measurements.tsv 939db602f9ef93849ea6c67da488e9883383ec6a5a7644a588fcc7bbc47a3385
```

원본과 스킬 파일은 수정하지 않았다. 이번 기록은 입력 점검 후 작성한 최초 설계이며, 향후 배치 정의나 교차 관측이 추가되면 해당 근거와 변경일, 이미 본 결과의 범위를 함께 기록하여 설계를 갱신한다.

