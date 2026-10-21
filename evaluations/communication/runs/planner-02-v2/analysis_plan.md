# 배치를 고려한 처리 효과 분석 설계

작성일: 2026-10-21. 범위: 제공 자료의 가벼운 전수 점검과 분석 설계. **현 자료에서는 처리 효과와 배치 효과를 분리할 수 없다.** 우선 권고는 관측된 두 집단의 차이를 기술하고, 처리 효과 추론에는 조건이 배치 내에서 교차하는 자료를 확보하는 것이다. 이번 요청에서는 아래 후속 분석을 실행하지 않았다.

## 연구 질문과 해석 범위

질문은 “사람 유래 배양 세포에서 동일 배양 조건의 24시간 처리 후, control에 비해 treated의 marker별 정규화된 log2 intensity가 얼마나 달라지는가?”이다. 독립 실험 단위는 donor, 관측 단위는 donor별 한 번의 표본 측정이며, 비교 방향은 **treated − control**이다. 두 marker 모두 계획 대상이며 특정 marker를 결과에 따라 우선 선택하지 않는다.

이 설계가 해결해야 할 결정은 관측 차이를 처리에 귀속할 수 있는지, 아니면 배치가 교차하는 추가 실험이 필요한지이다. 현재 가능한 양은 **treated/배치 B의 3명과 control/배치 A의 3명 사이의 관측 차이**다. 분리된 처리 효과, 인과적 처리 효과, 작동 기전은 이 자료로 결론 내릴 수 없다. 합성 자료이므로 아래 설계 점검은 실제 생물학적 효과의 검증도 아니다.

계획 작성 전에 입력 전체와 측정값 범위를 확인했다. 따라서 결과를 보지 않고 사전 등록한 계획으로 표현하지 않는다. 효과 추정, 가설검정, 차등발현 분석, 배치 보정은 수행하지 않았다.

## 확인된 근거와 남은 정보

입력 경로는 모두 `/tmp/bio-comm-20261021-planner-v2/` 아래이며 원본을 변경하지 않았다.

| 근거 구분 | 출처·실제 확인 범위 | 분석에 미치는 영향 |
| --- | --- | --- |
| 제공 기록의 사실 | `context.md` 전체: 합성 bulk marker, 정규화된 log2 intensity, 사람 유래 배양 세포, 독립 donor 6명, 24시간 처리, 기술 반복 없음 | count 자료가 아니다. 다시 log 변환하거나 반올림해 count 모형에 넣지 않는다. 독립성은 제공 기록에 근거하며 원실험 기록으로 별도 검증한 것은 아니다. |
| 파일에서 직접 확인 | `metadata.tsv` 전체 6행과 `measurements.tsv` 전체 2행 × 6열: 표본 ID 일치, 중복 표본·marker 및 반복 donor ID 없음 | control 3명, treated 3명의 비대응 설계다. C1/T1 등의 이름이나 열 순서로 짝을 만들지 않는다. |
| 파일에서 직접 확인 | metadata 빈 필드 0, 측정값 12개 모두 유한, 0값 없음, 범위 4.8–8.7, 행 너비 오류 없음 | 결측 대체나 임의의 저값 필터 없이 두 marker를 보존한다. 이 확인이 측정 정확도나 정규화 적절성을 입증하지는 않는다. |
| 핵심 설계 제약 | `metadata.tsv` 전수 교차표: control은 A에만, treated는 B에만 존재 | 조건별 donor n은 3이지만 조건별 배치 n은 1이다. 배치를 고려한 독립 처리 비교는 불가능하다. |
| 임시 가정 | 제공된 값이 표본 간 같은 단위로 비교 가능한 정규화 log2 intensity라고 보고 기술 요약만 계획 | 원래 intensity의 정의와 정규화 절차가 다르면 비교 단위부터 수정한다. 차이의 단위는 log2 intensity이며 보정·배경처리 정보 없이 분자량의 배수 변화로 단정하지 않는다. |
| 미해결 | 정규화 방법, 배치 A/B가 뜻하는 실험·측정 단계, 원시 측정/QC 기록, 조건 배정·무작위화 기록, 처리 물질·용량·대조군 내용, donor 특성, 미제공 교차 표본의 존재 | 기록 오기인지 실제 완전 교락인지, 측정 단위가 비교 가능한지 확인해야 한다. 배정 정보가 없으므로 설계가 교차하더라도 인과적 해석은 별도 조건이 필요하다. |

확인된 교차표의 단위는 **고유 donor 수**다.

| condition | batch A | batch B | 합계 |
| --- | ---: | ---: | ---: |
| control | 3 | 0 | 3 |
| treated | 0 | 3 | 3 |

각 표본에서 `I(treated)`와 `I(batch B)`가 완전히 동일하다. 예를 들어 `intensity = 절편 + 처리계수 × I(treated) + 배치계수 × I(batch B)`에서 자료가 구분할 수 있는 것은 두 계수의 합뿐이다. 이는 적합 결과가 아니라 확인된 설계의 대수적 성질이다. donor마다 한 번만 측정했으므로 donor별 고정효과를 추가하는 방식도 이 문제를 해결하지 않는다. 배치 보정 알고리즘이나 같은 구조의 donor 증원으로 분리된 효과가 생기지 않는다.

## 권고 경로와 결과에 따른 분기

| 과학적 질문·필요한 이유 | 필요한 입력과 최소 방법 | 확인할 산출물 | 결과에 따른 결정과 한계 |
| --- | --- | --- | --- |
| 배치 교락이 실제 실험 구조인가? 효과 추론의 가능성을 결정한다. | 현재 `context.md`, `metadata.tsv`를 실험·측정 배치 원장 및 표본 배정 기록과 대조한다. 배치의 단계와 실제 교차 표본 유무를 확인한다. 원장은 현재 제공되지 않았다. | 표본별 실제 처리·배치·donor 대응표, 수정 근거, 갱신된 조건×배치 donor 수 | 기록이 맞으면 아래 기술 분석만 유지한다. 오기 또는 누락된 교차 표본이 증거로 확인되면 원본을 보존한 정정 표를 만들고 설계를 다시 확인한다. 확인되지 않으면 현재 교락을 유지하며 임의로 배치를 삭제하지 않는다. |
| 지금 관측되는 차이의 크기와 donor 분포는 어떠한가? 추가 실험의 필요성을 설명할 기초 요약이다. | 현재 두 TSV를 ID로 연결한다. marker별 두 집단의 개별 값, n, 평균, SD, 최솟값·최댓값, 평균 차이(B-treated − A-control)를 계산한다. 추가 정규화는 하지 않는다. | 2행 요약표와 marker별 donor 점도표. 축은 log2 intensity, 집단명에 조건과 배치를 함께 표기하고 같은 donor를 연결하는 선은 쓰지 않는다. | 차이가 크고 집단 내 일관되어도 처리/배치 중 원인을 구분하지 못한다. 겹침이 크거나 한 donor가 분포를 좌우하면 그 불확실성을 기술하고 QC 기록을 확인한다. 차이가 작아도 처리 효과 부재를 뜻하지 않는다. 처리와 배치가 상쇄될 가능성도 구분할 수 없다. |
| 표본 간 척도와 측정 품질을 신뢰할 수 있는가? 관측 차이 자체의 의미를 확인한다. | 정규화·배경처리 절차, 원시 intensity와 사용 가능한 QC 지표/공통 기준 시료 기록을 확인한다. 낮거나 높은 값만으로 제외하지 않는다. | 단위·정규화 설명과 표본별 QC 근거 | 같은 비교 척도가 확인되면 기술 요약을 유지한다. 명확한 측정 오류가 확인되면 이유를 기록하고 해당 표본 포함/제외 요약을 함께 제시한다. 절차가 불명확하면 현재 값의 기술에 한정한다. 공통 기준 시료가 있더라도 그 사실만으로 생물학적 처리 효과가 식별된다고 보지 않는다. |
| 배치와 분리된 처리 차이를 새 자료에서 추정할 수 있는가? 본래 목표의 재시작 조건이다. | 독립 배치마다 두 조건을 모두 포함하고 각 조건에 복수 donor가 있도록 설계한다. 가능하면 동일 donor의 배양물을 두 조건으로 나누어 배치 내 무작위 배정하고 donor별 대응을 유지한다. 불가능하면 독립 donor를 조건과 배치에 균형 있게 무작위 배정한다. 적어도 복수 배치에서 조건 비교가 반복되게 하되 필요한 donor/배치 수는 목표 효과와 독립 분산 자료로 따로 설계한다. | 교차 설계표, 독립 donor 수, 대응 관계, 조건·배치 효과의 식별 가능성, 실험 배정 근거 | 조건 대비가 식별되고 척도/QC가 확인되면 연속형 log2 intensity에 맞는 배치 조정 비교를 설계한다. 대응 자료는 donor 내 차이를 보존하며 반복 측정을 독립 n으로 세지 않는다. 비대응 자료는 donor를 독립 단위로 둔다. 일부 교차만 확보되면 실제로 식별되는 대비와 남은 불균형을 검토한다. 계속 완전 교락이면 처리 효과 추론은 재개하지 않는다. |

현재 요약에서 SD와 범위는 **관측 집단 안의 donor 간 퍼짐**만 보여준다. 배치 간 변동이나 처리 효과의 불확실성을 대신하지 않는다. 조건당 배치가 하나이므로 donor 재표집으로 처리 효과 신뢰구간을 만들거나 p값으로 처리 효과를 판정하지 않는다. 현재 단계에 PCA, 클러스터링, 경로 풍부도 분석을 추가해도 핵심 식별 문제를 해결하지 못하므로 우선 경로에 포함하지 않는다.

새 교차 자료에서 추론을 재개할 경우, 처리−대조 추정치와 불확실성 구간을 log2 intensity 단위로 제시한다. 배치는 설계상 조정 변수이고, donor 관련 항은 실제 대응·반복 구조에 맞춰 정한다. donor 특성 공변량은 사전 근거와 표본 규모가 허용할 때만 검토하며 현 6명 자료에 많은 변수를 추가하지 않는다. marker별 검정이 목적이면 사전 지정한 두 marker를 하나의 다중검정 범위로 다룬다. 구체적 추정법·검정 보정법과 해당 공식 근거는 재시작 조건을 만족한 뒤 정하며, 현재 계획에서는 특정 도구의 적합성을 검증하지 않았다. 생물학적으로 의미 있는 변화 크기의 기준도 제공되지 않았으므로 관측값에 맞춰 임의로 만들지 않는다.

## 첫 후속 실행 단계와 필요한 자료

**바로 실행 가능한 후속 단계는 현재 두 집단의 기술 요약이다.** 입력은 `/tmp/bio-comm-20261021-planner-v2/metadata.tsv`와 `/tmp/bio-comm-20261021-planner-v2/measurements.tsv`이다. 표본 ID로 연결하여 위에서 정한 두 marker의 요약표와 6개 donor 점이 모두 보이는 그림을 만든다. 결과 라벨은 반드시 “treated/B − control/A의 관측 차이”로 유지한다. 확인 기준은 모든 표본이 포함되었고 척도·조건·배치가 명시되었는지, 개별 donor 분포와 요약치가 서로 일치하는지다. 분포에 따라 측정 QC 확인 필요성을 구분할 수 있으나 처리 대 배치의 원인을 판단할 수는 없다. 이 작업은 이번 설계 요청에서는 실행하지 않았다.

**처리 효과 추론의 첫 미해결 단계는 실험 기록 확인이다.** 필요한 것은 표본별 배양·처리 배정 원장, 측정 배치 원장, 정규화 절차와 원시/QC 자료다. 기존 기록에 다른 배치의 control 또는 treated가 있는지 확인한다. 존재하고 비교 가능한 기록이 확보되면 교차표를 재작성하여 설계를 검토하고, 없으면 위 교차 실험을 준비한다. 현재 파일만으로 이 기록 확인을 완료할 수 없다. 나머지 기술 비교 설계는 완료했으므로 이번 요청을 끝내기 위해 추가 승인을 요구하지 않는다.

## 완료 기준과 수행 기록

이번 산출물의 완료 기준은 실제 입력으로 독립 단위와 설계 제약을 확인하고, 가능한 비교·금지할 해석·분기·첫 후속 단계를 남기는 것이다. 이는 충족했다. **다음 기술 요약은 준비되었지만 처리 효과 추론은 차단되어 있다.** 이후 분석이 완료되려면 원본을 보존한 재실행 코드, marker별 관측값과 요약표/그림, 처리와 배치 분리가 가능한지의 근거, 제외나 기록 수정의 이유, 자료가 허용하는 수준의 결론을 함께 제시해야 한다. 식별되지 않거나 불확실하다는 결론도 유효한 결과다.

실제 수행: `TASK.md`, `context.md`, 두 TSV, 지정 스킬과 참고문서를 읽었다. 아래 Python 3.12.7 표준 라이브러리 코드로 TSV 전체의 ID 대응·중복·반복 donor·빈 필드·행 너비·값 범위·조건×배치 구성을 확인했다. 통계 모형, 효과 요약, 유의성 검정, 그림 생성, 외부 자료 검색·다운로드는 하지 않았다. 생물학적 독립성 및 실험 내용은 제공 설명 이상으로 검증하지 않았다. 2026-10-21 최초 계획이며 기존 계획 변경은 없다.

### 점검 재현 코드

아래 코드는 실제 실행한 점검 코드다. 출력 목적 설명을 코드 안에 포함했으며 입력을 읽기만 한다. `python3`에서 그대로 실행할 수 있다.

```python
from pathlib import Path
from collections import Counter
import csv
import hashlib
import math
import platform

root = Path('/tmp/bio-comm-20261021-planner-v2')
print('재현 정보: 입력을 변경하지 않는 전수 점검이며 Python 표준 라이브러리만 사용합니다.')
print('Python:', platform.python_version())
for name in ['TASK.md', 'context.md', 'metadata.tsv', 'measurements.tsv']:
    print(name, 'SHA256:', hashlib.sha256((root / name).read_bytes()).hexdigest())
with (root / 'metadata.tsv').open(newline='') as handle:
    metadata = list(csv.DictReader(handle, delimiter='\t'))
with (root / 'measurements.tsv').open(newline='') as handle:
    matrix = list(csv.reader(handle, delimiter='\t'))
samples = matrix[0][1:]
rows = matrix[1:]
metadata_samples = [row['sample_id'] for row in metadata]
donors = [row['donor_id'] for row in metadata]
features = [row[0] for row in rows]
print('\n표본 대응과 반복 관계: 측정 열과 metadata를 연결할 수 있는지, 독립 n이 몇 명인지 확인합니다.')
print('metadata 표본:', len(metadata), '| 측정 표본:', len(samples), '| marker:', len(features))
print('metadata 중복 표본:', len(metadata_samples) - len(set(metadata_samples)), '| 측정 중복 표본:', len(samples) - len(set(samples)))
print('측정에만 있는 표본:', len(set(samples) - set(metadata_samples)), '| metadata에만 있는 표본:', len(set(metadata_samples) - set(samples)))
print('고유 donor:', len(set(donors)), '| 반복 donor ID:', len(donors) - len(set(donors)), '| 중복 marker:', len(features) - len(set(features)))
print('metadata 빈 필드:', sum(value is None or value.strip() == '' for row in metadata for value in row.values()))
print('\n측정 형식: log2 intensity로 해석할 값이 유한한지 확인하며 재정규화나 모형 적합은 하지 않습니다.')
print('측정 행 너비 오류:', sum(len(row) != len(matrix[0]) for row in rows))
values = [float(value) for row in rows for value in row[1:]]
print('값 수:', len(values), '| 비유한값:', sum(not math.isfinite(value) for value in values), '| 0:', sum(value == 0 for value in values), '| 범위:', min(values), '–', max(values))
print('\n처리와 배치를 분리할 수 있는지 확인합니다. 표의 단위는 고유 donor 수입니다.')
conditions = ['control', 'treated']
batches = ['A', 'B']
print('condition\tbatch A\tbatch B\ttotal')
for condition in conditions:
    counts = [len({row['donor_id'] for row in metadata if row['condition'] == condition and row['batch'] == batch}) for batch in batches]
    print(condition, *counts, sum(counts), sep='\t')
treated_column = [int(row['condition'] == 'treated') for row in metadata]
batch_b_column = [int(row['batch'] == 'B') for row in metadata]
print('treated 지시열과 batch B 지시열이 동일:', treated_column == batch_b_column)
print('동일하면 두 계수를 별도로 추정할 설계 정보가 없습니다. 이 점검은 효과 추정이나 검정이 아닙니다.')
```

실행 결과의 수치와 교차표는 위 근거 표에 모두 반영했다. 입력 보존 및 동일 자료 재실행 확인용 SHA256은 다음과 같다.

```text
Python: 3.12.7
TASK.md         7ac0a21c29814e549bc3c2867e30c70008852be4d840cc32b69a4cfee0293c83
context.md      540bce3b2ba0f37c8bab222e640e21d98098c70d7a6469ea887dcda58d20f4e4
metadata.tsv    a3e6dd70a4f26218d386f7b909505eb22be0da922a1b53a942c1123698a0014f
measurements.tsv 939db602f9ef93849ea6c67da488e9883383ec6a5a7644a588fcc7bbc47a3385
```
