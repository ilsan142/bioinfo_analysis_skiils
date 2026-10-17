#!/usr/bin/env python3
"""Audit the supplied synthetic design and summarize its observable contrast.

Run from this directory: python analyze.py > analysis_record.md
No external data, model fit, stochastic operation, or input modification.
"""
import csv
import hashlib
import platform
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_table(name):
    path = ROOT / name
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    require(len(rows) > 1, f"{name}: empty table")
    require(len(rows[0]) == len(set(rows[0])), f"{name}: duplicate header")
    require(all(len(row) == len(rows[0]) for row in rows), f"{name}: ragged rows")
    require(all(value and value == value.strip() for row in rows for value in row),
            f"{name}: blank value or surrounding whitespace")
    return pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)


meta = read_table("metadata.tsv")
data = read_table("measurements.tsv")
require(list(meta.columns) == ["sample_id", "donor_id", "condition", "batch"],
        "Unexpected metadata columns")
require(data.columns[0] == "feature_id", "First measurement column must be feature_id")
require(meta.sample_id.is_unique, "Duplicate sample IDs")
require(meta.donor_id.is_unique, "Repeated donors: revisit the independent-unit assumption")
require(data.feature_id.is_unique, "Duplicate feature IDs")
require(set(meta.condition) == {"control", "treated"}, "Unexpected conditions")
require(set(meta.batch) == {"A", "B"}, "Unexpected batches")
require(set(meta.sample_id) == set(data.columns[1:]), "Sample IDs do not match")
values = data.set_index("feature_id").apply(pd.to_numeric, errors="raise")
# The join uses IDs explicitly, so measurement-column order cannot alter groups.
values = values.loc[:, meta.sample_id.tolist()]
require(np.isfinite(values.to_numpy()).all(), "Non-finite measurements")

treated = (meta.condition == "treated").to_numpy(dtype=int)
batch_b = (meta.batch == "B").to_numpy(dtype=int)
design = np.column_stack([np.ones(len(meta)), treated, batch_b])
rank = int(np.linalg.matrix_rank(design))
require(rank == 2 and np.array_equal(treated, batch_b),
        "Design changed: reassess identifiability before using this report")
null_residual = design @ np.array([0, 1, -1])
require(np.array_equal(null_residual, np.zeros(len(meta))), "Null-vector check failed")
cross = pd.crosstab(meta.condition, meta.batch).reindex(
    index=["control", "treated"], columns=["A", "B"], fill_value=0)

records = []
for feature, row in values.iterrows():
    entry = {"feature_id": feature}
    for condition in ["control", "treated"]:
        sample_ids = meta.loc[meta.condition == condition, "sample_id"]
        group = row.loc[sample_ids]
        require(len(group) >= 2, "At least two independent observations are needed for SD")
        entry.update({f"{condition}_n_donors": len(group),
                      f"{condition}_mean_log2_intensity": float(group.mean()),
                      f"{condition}_sd_log2_intensity": float(group.std(ddof=1)),
                      f"{condition}_min_log2_intensity": float(group.min()),
                      f"{condition}_max_log2_intensity": float(group.max())})
    entry["observed_treatedB_minus_controlA_log2_intensity"] = (
        entry["treated_mean_log2_intensity"] - entry["control_mean_log2_intensity"])
    entry["batch_adjusted_treatment_effect_status"] = "not_identifiable"
    records.append(entry)
summary = pd.DataFrame(records)
summary.to_csv(ROOT / "descriptive_results.tsv", sep="\t", index=False, float_format="%.6f")

print("# 처리 효과와 배치의 분리 가능성: 실행 기록\n")
print("## 질문과 결론\n")
print("관심 비교는 24시간 treated − control의 처리 효과이며 배치를 고려하려는 것이다. "
      "모든 control은 배치 A, 모든 treated는 배치 B에 있어 처리 효과와 배치 효과가 완전히 겹친다. "
      "이 자료로 배치 보정 처리 효과는 식별 불가능하다. 이는 효과가 없다는 결론이 아니다.\n")
print("## 입력과 확인된 사실\n")
print("자료 의미와 실험 설계는 제공된 context.md를 따른다. 합성 bulk marker 자료이며, "
      "값은 이미 정규화된 log2 intensity이다. 행은 가상 marker, 열은 sample ID이다. "
      "사람 유래 배양 세포의 독립 donor 6명을 각 한 번 측정했고, "
      "control과 treated는 동일 배양 조건에서 24시간 처리를 비교한다. 기술 반복은 없다. "
      "실제 생물학적 검증 자료가 아니다.\n")
print(f"- 샘플 {len(meta)}개, marker {len(values)}개. 각 군의 독립 단위는 서로 다른 donor 3명이다.")
print("- 샘플·donor·feature ID와 원시 TSV 헤더 중복 없음; 표 행 길이 일치; 빈 값 없음.")
print("- 측정표와 메타데이터의 sample ID 집합 일치. sample ID로 순서를 맞췄다.")
print(f"- 측정값 모두 유한한 수; 전체 범위 {values.min().min():.1f}–{values.max().max():.1f} log2 intensity.")
print("- 샘플/marker 제외, 재정규화, 추가 로그 변환, 반올림 입력 변환, 대치, 집계 없음. "
      "분석 전후 6개 샘플과 2개 marker를 그대로 유지했다.\n")
print("```text\n" + cross.to_string() + "\n```\n")
print("## 실행 순서와 의사결정\n")
print("1. 입력의 의미와 독립 단위를 확인하고 식별자·결측·값·조건×배치 배치를 점검했다.")
print("2. [절편, treated 대 control, batch B 대 A] 설계행렬의 rank와 null vector를 계산했다.")
print("3. rank=2/열 3개라는 출력을 확인한 뒤, 처리 효과 추론을 진행하지 않고 "
      "관측 차이와 군 내 산포를 기술하는 분석을 작성·실행했다. 이 전환은 설계 점검에 따른 결정이다.\n")
print("```text\n설계행렬 열: intercept, treated_vs_control, batch_B_vs_A")
print(design.astype(int))
print(f"rank = {rank}; columns = {design.shape[1]}")
print(f"X @ [0, 1, -1] = {null_residual.astype(int).tolist()}\n```\n")
print("모형을 y = α + τ·treated + β·batch_B로 쓰면 treated= batch_B이므로 "
      "α + (τ+β)·treated만 관측된다. 어떤 상수 c에 대해서도 (τ+c, β−c)가 "
      "같은 예측을 만든다. 배치 효과를 제거하거나 처리 효과를 분리할 유일한 해가 없다.\n")
print("## 관측 결과\n")
print("| Marker | Control/A 평균 ± SD (n) | Treated/B 평균 ± SD (n) | 관측 차이: treated/B − control/A |")
print("|---|---:|---:|---:|")
for row in records:
    print(f"| {row['feature_id']} | {row['control_mean_log2_intensity']:.2f} ± "
          f"{row['control_sd_log2_intensity']:.2f} ({row['control_n_donors']}) | "
          f"{row['treated_mean_log2_intensity']:.2f} ± {row['treated_sd_log2_intensity']:.2f} "
          f"({row['treated_n_donors']}) | "
          f"{row['observed_treatedB_minus_controlA_log2_intensity']:+.2f} |")
print("\n평균·SD·관측 차이의 단위는 log2 intensity이며 SD는 각 군 donor 3명 사이의 표본 표준편차(ddof=1)이다. "
      "SD는 처리 효과의 표준오차나 신뢰구간이 아니다. "
      "두 marker 모두 treated/B에서 높은 관측값을 보이지만, 처리와 배치 중 어느 원인인지는 구분할 수 없다. "
      "정규화 방식의 세부 정보가 없으므로 원래 절대 양의 변화나 기전으로 해석하지 않았다.\n")
print("## 실행하지 않은 추론과 한계\n")
print("배치 보정 회귀계수, 처리 효과 p-value, 신뢰구간, 차등 marker 선정 및 FDR 보정을 산출하지 않았다. "
      "유효한 처리 효과 검정군 자체를 정의해 실행하지 않았으므로 다중검정 보정은 해당하지 않는다. "
      "의사역행렬, 배치항 삭제, 배치 보정 알고리즘으로 결측 설계 조합을 대신하지 않았다. "
      "조건과 배치가 겹치는 구조를 유지한 채 donor 수만 늘려도 이 식별성 문제는 해소되지 않는다. "
      "군당 donor가 3명뿐이고 실제 할당의 무작위화, 배치 발생 단계, 정규화 방법의 세부 정보는 제공되지 않았다.\n")
print("## 다음 확인 사항\n")
print("- 원 실험/처리 기록에서 batch의 의미, 조건 배정과 sample ID를 확인한다. "
      "메타데이터 오류가 확인되는 경우에만 수정하고 분석을 다시 수행한다.")
print("- 실제로 완전 교락이라면 각 배치에 control과 treated가 모두 포함되도록 후속 설계를 구성한다. "
      "기술 반복만 추가하지 말고 충분한 독립 donor를 포함하고 조건과 처리 순서를 무작위화한다. "
      "가능하면 각 donor의 세포를 두 조건으로 나누어 배치 내 비교를 만들되, "
      "이 경우 donor를 짝지어진 독립 단위로 취급하고 반복 측정을 독립 n으로 세지 않는다.")
print("- 정규화 방법, 배치 발생 단계, 추가 시료 접근성을 확인한 뒤 공통 배치 안의 비교와 "
      "처리×배치 상호작용을 평가할 수 있는 복제 구조를 정한다. "
      "새 자료가 생기면 설계행렬을 다시 확인하고 목표 효과 크기와 분산을 바탕으로 표본 수를 정한다.\n")
print("## 재실행과 산출물\n")
print("```bash\ncd /tmp/bio-skill-en-03\npython analyze.py > analysis_record.md\n```\n")
print("위 명령으로 입력 전체를 읽고 점검 및 요약을 처음부터 실행했다. "
      "환경 설치, 외부 데이터/문헌 조회, 난수 사용은 없었다. "
      "별도의 그림은 만들지 않았으며 작은 표로 결과와 설계 문제를 확인했다. "
      "이 기록은 표준 출력이며 실행 실패는 숨기지 않고 표준 오류로 전파한다.\n")
print(f"환경: Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}.\n")
print("- analyze.py: 입력 검사, 설계행렬 계산, 기술 통계와 이 기록을 재생성하는 코드.")
print("- descriptive_results.tsv: 군별 n·평균·SD·범위, 관측 차이, 처리 효과 식별 불가 상태.")
print("- analysis_record.md: 실행 명령, 실제 결과, 의사결정, 한계와 후속 확인 사항.\n")
print("SHA-256 (입력·코드 식별):\n")
print("```text")
for name in ["TASK.md", "context.md", "metadata.tsv", "measurements.tsv", "analyze.py"]:
    print(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), name)
print("```")
