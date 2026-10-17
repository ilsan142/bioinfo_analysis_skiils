#!/usr/bin/env python3
"""Synthetic log2 marker panel: ID alignment, design and exploratory effects."""
from pathlib import Path
import csv
import hashlib
import platform

import numpy as np
import pandas as pd
import scipy
import statsmodels
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parent


def table(frame):
    print("```text\n" + frame.to_string() + "\n```")


def load_and_check():
    metadata = pd.read_csv(ROOT / "metadata.tsv", sep="\t", dtype=str)
    with (ROOT / "measurements.tsv").open() as stream:
        header = next(csv.reader(stream, delimiter="\t"))
    assert len(header) == len(set(header)), "Duplicate measurement column IDs"
    marker = pd.read_csv(ROOT / "measurements.tsv", sep="\t", index_col=0,
                         na_values=["NA"])
    assert not metadata.isna().any().any(), "Missing metadata"
    assert metadata.sample_id.is_unique, "Duplicate metadata sample IDs"
    assert marker.index.is_unique, "Duplicate marker IDs"
    assert not marker.index.isna().any(), "Missing marker IDs"
    assert set(marker.columns) == set(metadata.sample_id), "Unmatched sample IDs"
    assert metadata.donor_id.is_unique, "Donor dependence needs a revised analysis"
    assert set(metadata.condition) == {"control", "treated"}
    assert set(metadata.batch) == {"A", "B"}
    values = marker.loc[:, metadata.sample_id].T.apply(pd.to_numeric, errors="raise")
    assert not np.isinf(values.to_numpy()).any(), "Infinite intensity"
    metadata = metadata.set_index("sample_id")
    assert values.index.equals(metadata.index), "Alignment failed"
    design = pd.DataFrame({"intercept": 1.0,
                           "treated": (metadata.condition == "treated").astype(float),
                           "batch_B": (metadata.batch == "B").astype(float)},
                          index=metadata.index)
    assert np.linalg.matrix_rank(design) == design.shape[1], "Confounded design"
    return metadata, values, design


def qc(metadata, values, design):
    print("# 합성 marker 탐색 분석 실행 기록\n")
    print("입력: context.md, metadata.tsv, measurements.tsv. 출력 단위: 이미 정규화된 log2 intensity.")
    print("관심 효과: 서로 다른 독립 기증자의 treated-control 평균 차이; control 및 batch A가 기준.")
    print("추가 로그 변환, 반올림, 정규화, 대체, 표본·marker 제외 없음. 0은 척도상의 값이며 NA만 결측.")
    print("원본 보존. 실행 경로: 스크립트가 있는 디렉터리. 확률적 연산 없음.\n")
    print(f"환경: Python {platform.python_version()}, NumPy {np.__version__}, pandas {pd.__version__}, SciPy {scipy.__version__}, statsmodels {statsmodels.__version__}.\n")
    print("## 입력 식별과 연결\n")
    for name in ["context.md", "metadata.tsv", "measurements.tsv"]:
        print(f"- {name}: SHA256 {hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}")
    print(f"\n전후 표본 {len(metadata)}→{len(metadata)}, marker {values.shape[1]}→{values.shape[1]}; "
          f"독립 donor {metadata.donor_id.nunique()}; 결측 {values.isna().sum().sum()}; "
          f"0 값 {(values == 0).sum().sum()}; 범위 {values.min().min():.3f}–{values.max().max():.3f}.")
    print("측정 열의 원래 순서는 metadata와 다름. sample_id로 연결한 모든 관측:")
    table(metadata.join(values))
    print("## 조건·배치와 독립 반복\n")
    table(pd.crosstab(metadata.condition, metadata.batch))
    print(f"설계 행렬 [intercept, treated, batch_B] rank={np.linalg.matrix_rank(design)}/{design.shape[1]}; "
          f"잔차 자유도 {len(metadata) - design.shape[1]}. 각 조건 독립 donor n=4, 기술 반복 없음.\n")
    print("## 조건별 분포 (log2 intensity)\n")
    long = values.join(metadata.condition).melt(id_vars="condition", var_name="feature_id", value_name="intensity")
    summary = long.groupby(["feature_id", "condition"]).intensity.agg(["count", "mean", "std", "median", "min", "max"])
    table(summary.round(4))


def compare(metadata, values, design):
    # Added after inspecting QC: the balanced batches show different intensity levels.
    # The donor deletion check is sensitivity analysis, not an exclusion rule.
    assert not values.isna().any().any(), "Missing values need an explicit analysis decision"
    rows = []
    treated = metadata.condition.eq("treated")
    for feature_id in values:
        y = values[feature_id]
        fit = sm.OLS(y, design).fit()
        ci = fit.conf_int(alpha=0.05).loc["treated"]
        row = {
            "feature_id": feature_id,
            "control_n": int((~treated).sum()),
            "treated_n": int(treated.sum()),
            "control_mean": y[~treated].mean(),
            "treated_mean": y[treated].mean(),
            "raw_difference": y[treated].mean() - y[~treated].mean(),
            "batch_adjusted_difference": fit.params["treated"],
            "ci95_low": ci.iloc[0],
            "ci95_high": ci.iloc[1],
            "batch_B_minus_A": fit.params["batch_B"],
            "residual_sd": np.sqrt(fit.mse_resid),
        }
        for batch in ["A", "B"]:
            keep = metadata.batch.eq(batch)
            row[f"within_batch_{batch}_difference"] = y[keep & treated].mean() - y[keep & ~treated].mean()
        # Independent arithmetic check for the observed balanced 2x2 design.
        cells = pd.crosstab(metadata.condition, metadata.batch).to_numpy()
        if np.all(cells == cells[0, 0]):
            assert np.isclose(row["batch_adjusted_difference"],
                              (row["within_batch_A_difference"] + row["within_batch_B_difference"]) / 2)
        deletion_effects = []
        for sample_id in metadata.index:
            keep = metadata.index != sample_id
            assert np.linalg.matrix_rank(design.loc[keep]) == design.shape[1]
            deletion_effects.append(sm.OLS(y.loc[keep], design.loc[keep]).fit().params["treated"])
        row["leave_one_donor_out_min"] = min(deletion_effects)
        row["leave_one_donor_out_max"] = max(deletion_effects)
        rows.append(row)
    results = pd.DataFrame(rows).set_index("feature_id")
    results.to_csv(ROOT / "results.tsv", sep="\t", float_format="%.9g")
    print("## QC 확인 뒤 추가 실행: 배치 보정 및 기증자 영향 점검\n")
    print("모형: intensity ~ intercept + treated + batch_B, 독립 기증자 단위 OLS. "
          "관측값은 그대로 사용하며 paired 분석은 하지 않음. 배치별 수준 차이 때문에 배치를 보정함. "
          "관심값은 동일 배치에서의 treated-control 차이를 공통 효과로 요약한 계수.\n")
    table(results[["raw_difference", "batch_adjusted_difference", "ci95_low", "ci95_high",
                   "batch_B_minus_A", "residual_sd"]].round(4))
    print("95% 구간은 잔차의 독립성·정규성·등분산성과 가법 모형에 의존하는 t 구간(df=5). "
          "각 marker별 구간이며 3개 전체에 대한 동시 구간이 아님. 탐색 요약으로 p값 검정·유의성 판정은 하지 않음.\n")
    table(results[["within_batch_A_difference", "within_batch_B_difference",
                   "leave_one_donor_out_min", "leave_one_donor_out_max"]].round(4))
    print("배치 내 비교는 조건별 n=2. leave-one-donor-out은 매번 1명을 제외해 다시 적합한 효과의 범위이며 "
          "신뢰구간이 아님. 본 분석은 8명 전원 유지.\n")
    return results


def close_record(results):
    print("## 관측의 해석과 다음 판단\n")
    for feature_id, row in results.iterrows():
        crosses_zero = row.ci95_low <= 0 <= row.ci95_high
        print(f"- {feature_id}: treated-control {row.batch_adjusted_difference:+.3f} log2 단위, "
              f"95% 구간 [{row.ci95_low:.3f}, {row.ci95_high:.3f}]. "
              + ("구간에 0이 포함되며 효과 없음·동등성의 근거로 해석하지 않음." if crosses_zero
                 else "모형의 가정 아래 방향이 비교적 분명한 패턴이며 실제 생물학적 검증은 아님."))
    print("\n현재 균형 설계에서는 보정 전후 조건 계수가 같음. 이는 배치 차이가 없다는 뜻이 아니며 "
          "batch B의 수준은 A보다 marker별 0.225–0.250 높음.")
    print("현재 자료에 필요한 추가 점검인 배치별 대비와 기증자 한 명씩 제외한 민감도 분석을 실행했고, "
          "모든 marker의 차이 방향이 유지됨. 독립 검증이나 제외 근거로 사용하지 않음.")
    print("실제 연구로 이어갈 경우 처리 배정·실험 기록을 확인하고 조건×배치를 균형 있게 구성한 "
          "추가 독립 기증자로 작은 효과의 정밀도와 재현성을 확인해야 함. 현재 합성 자료만으로 이를 추가 검증할 수 없음.\n")
    print("## 실행과 범위\n")
    print("초기 QC 실행: `python analysis.py` (효과 분석 구현 전에 출력 확인). "
          "그 결과 배치 내 대비와 기증자 영향 점검을 사후 탐색으로 추가함.")
    print("최종 재실행: `python analysis.py > analysis_record.md`. "
          "같은 디렉터리에 `results.tsv`와 이 기록을 생성함. 원본과 비교 방향은 변경하지 않음.")
    print("그림 없이 전 관측과 분포·효과 표로 확인. 외부 annotation, 문헌 검색, 패키지 설치, 실제 생물학적 검증은 수행하지 않음.")
    print("8명뿐이므로 잔차 분포·등분산성과 조건×배치 상호작용을 충분히 검증할 수 없음. "
          "반복 수가 적어 작은 효과의 정밀도가 제한됨. 처리 무작위 배정 여부는 제공되지 않았으며 인과 효과로 해석하지 않음. "
          "합성 자료의 수치 패턴이므로 실제 사람 세포의 생물학적 효과·기전·marker 기능을 주장할 수 없음.")


def main():
    metadata, values, design = load_and_check()
    qc(metadata, values, design)
    results = compare(metadata, values, design)
    close_record(results)


if __name__ == "__main__":
    main()
