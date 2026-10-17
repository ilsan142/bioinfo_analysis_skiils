# 검증 기록 — 2026-10-17

> **Current edition:** The distributable skill is now in English. Translation checks are recorded in [ENGLISH_EDITION.md](ENGLISH_EDITION.md), and the subsequent notebook-workflow update in [NOTEBOOK_WORKFLOW.md](NOTEBOOK_WORKFLOW.md). The Korean record below describes the earlier Korean v1/v2 editions; it is not evidence that every scenario was rerun after these updates.

실제 연구 자료는 사용하지 않았다. **6종의 작은 사례에서 에이전트 행동을 실행해 관찰했고, 4종은 시나리오 검토만 했다.** 정상 사례는 지침 수정 후 새 에이전트로 다시 실행했다. 표본 관계 정정 사례는 초기 분석 뒤 정정 입력을 전달하는 두 차례 작업이었다. 이는 스킬의 제한된 행동 검증이지 생물학적 검증이 아니다.

## 방법과 버전

- `skill-creator`의 작성·독립 실행 검증 절차와 `quick_validate.py`를 사용했다. 공통 스킬은 `skills/bioinformatics-research-assistant/`의 문서 4개다.
- 빈 작업 공간과 상위 경로에 적용되는 `AGENTS.md`가 없음을 먼저 확인했다. 기존 연구 분석이나 사용자 전역 설정은 변경하지 않았다.
- 각 실행은 부모 대화를 넘기지 않은 새 에이전트(`fork_turns=none`)에 스킬·해당 TASK.md·그 사례의 입력 파일만 제공했다. 채점 기준, 기대 수치, 의심한 문제와 다른 사례는 전달하지 않았다. 사례 07의 정정만 후속 입력으로 전달했다.
- 사례 10에는 스킬의 name·description·경로만 노출했다. 사용하거나 읽도록 강제하지 않았다.
- 작업은 `/tmp/bio-skill-eval-*`로 제한하도록 지시했다. 물리적 파일시스템 격리는 아니며, 에이전트들은 동일 실행 환경을 공유했다. 공개 도구 기록에서 평가 기준/다른 프로젝트를 읽은 흔적은 없었다.
- 최초 지침은 [skill-v1](runs/skill-v1/SKILL.md), 해시는 [v1](runs/skill-v1.sha256.json)에 보존했다. 정상 사례에서 작은 요약을 여러 결과 파일로 분리한 것을 보고, 기존 표/기록에 통합하도록 문장 하나를 추가했다. 당시 한국어 배포 버전은 v2였으며 [당시 파일 해시](runs/skill-v2.sha256.json)를 남겼다.
- v2는 정상 사례만 재평가했다. 나머지 실행은 v1의 증거다. 스킬의 효과를 분리하는 무스킬 대조군이나 반복 시행에 의한 성공률 추정은 하지 않았다.

## 형식 검증

실행 명령:

```bash
python3 /home/ilsan/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/bioinformatics-research-assistant
python3 evaluations/validate_package.py
```

확인 범위는 YAML `name`·`description`, 이름/폴더 일치·길이, 미완성 scaffold, 로컬 문서 링크, Markdown fence·공백, 10개 입력과 단계적 정정 입력 구조다. 결과는 [format_checks.txt](runs/format_checks.txt)에 저장했다. 이 검사는 과학적 판단·실제 제품 검색·자동 선택을 증명하지 않는다. 당시 작업 공간은 Git 저장소가 아니어서 `git diff --check` 대신 로컬 파일의 공백·fence·링크를 검사했다.

## 실제 행동 평가

공통 기준은 도구 호출 순서, 출력과 코드·설명 일치, 불필요한 승인 요청, 원본 보존, 수행/미수행 구분으로 검토했다. 핵심 과학적 실패는 관찰되지 않았다. 모든 생물학적 자료는 합성이며 사례 06은 실제 모델 학습이 아닌 분할표 실행 점검과 코드 정적 검토다.

| ID / 버전 | 실제 관측과 판정 | 증거 |
| --- | --- | --- |
| 01 / v1 | 8/8 ID 연결, 독립 donor 군당 4, 각 조건×배치 2. 실제 점검 후 비교·민감도 분석을 차례로 추가했다. 효과 A/B/C=+1.025/+0.1/−0.1. 과학 판단·단계 진행은 통과. 작은 요약이 결과 파일 6개로 분산되어 산출물 정리 규칙을 개선했다. | [결과](runs/01-v1/RESULTS.md), [공개 실행 기록](runs/01-v1/public_trace.jsonl) |
| 01 / v2 | 새 에이전트가 동일 효과·95% 구간을 산출했다. donor별 제외 시 A=+0.98~+1.06. 승인 반복 없이 출력 확인 뒤 후속 구현. 코드·결과표·분석 기록 3개 파일로 통합해 수정 의도도 관찰했다. | [기록](runs/01-v2/analysis_record.md), [표](runs/01-v2/results.tsv), [실행 순서](runs/01-v2/public_trace.jsonl) |
| 02 / v1 | 3×4, 비정수 10/12, 0 한 개를 실제 확인. 원값 보존, 입력 종류·독립 n 미확인 표시. 기술적 평균차이만 제시하고 검정·반올림 보류. 필요한 생성/설계 정보와 이유 명시. 통과. 추가 정보에 대한 사용자의 응답 처리까지 시험한 것은 아니다. | [기록](runs/02-v1/ANALYSIS_RECORD.txt), [실행 순서](runs/02-v1/public_trace.jsonl) |
| 03 / v1 | 조건×배치 3/0, 0/3; 설계 rank 2/3. 관측 차이 A=+2, B=+0.5를 처리 고유 효과와 구분. 배치 보정으로 해결됐다는 주장 없이 추정 보류. 통과. | [기록](runs/03-v1/report.md), [감사 결과](runs/03-v1/results/audit.json), [실행 순서](runs/03-v1/public_trace.jsonl) |
| 06 / v1 | train/test 환자 중복 2명, 새로운 test 환자 0명. 전체 X/y의 특징 선택과 patient_id 미사용을 각각 확인. 실제 X/y가 없으므로 성능 수치 미산출. manifest와 실제 실행의 대응도 미확인이라고 구분. 통과. | [검토](runs/06-v1/review.md), [감사](runs/06-v1/audit_results.json), [실행 순서](runs/06-v1/public_trace.jsonl) |
| 07 / v1 | 초기 8명 독립 분석 뒤 명시적 pair 정정을 받음. 4 donor pairs·df=3으로 코드·메타데이터·표·기록을 갱신. A 평균 1.025 유지, SE 0.060208→0.047871, CI [0.870230,1.179770]→[0.872652,1.177348]. B/C의 pair 차이 0분산은 퇴화 사례로 표시하고 통상 CI 보고를 보류. 이전 결과 대체 표시·원본 보존. 통과. 그림은 생성하지 않아 그림 갱신은 적용 제외. | [이전 표](runs/07-before/results/contrasts.tsv), [새 표](runs/07-after/results/contrasts.tsv), [정정 기록](runs/07-after/analysis_record.txt), [실행 순서](runs/07-after/public_trace.jsonl) |
| 10 / metadata | 일반 HTML/CSS 요청을 수행하고 생물정보학 본문을 읽거나 연구/QC 질문을 하지 않았다. metadata만 제공한 제한된 선택 실험에서 통과. 제품 자체의 스킬 탐색 테스트는 아니다. HTML 구조는 점검했지만 브라우저 렌더링은 미검증으로 명시했다. | [실행 순서](runs/10-v1/public_trace.jsonl), [작업 기록](runs/10-v1/검증.txt) |

공개 실행 기록은 도구 호출·출력과 사용자에게 보이는 설명을 추출했다. 비공개 추론, 시스템 프롬프트, 암호화된 내부 조정 메시지는 포함하지 않았다. 원본 기록의 `/tmp/` 경로는 실행 당시 위치를 나타낸다. 복사된 코드와 결과는 이 `runs/` 아래 보존돼 있다.

## 재실행과 결과 대조

별도 임시 디렉터리에 코드·입력을 복사하여 새 Python 프로세스로 **7회 재실행**했다: 01-v1, 01-v2, 02, 03, 06, 07-정정 전/후. 모두 종료 코드 0이었다. 비교한 결과 파일은 동일했다(06의 실행 시각 필드만 비교에서 제외). 정상 효과, 완전 혼동 rank, 소수값 수, 환자 중복, paired n·df·SE·CI를 별도 계산/기대값과 대조했다. 모든 보존된 원본 입력이 cases.json과 일치했다. [재실행 결과](runs/replay_checks.json)

재현 명령 예:

```bash
cd evaluations/runs/01-v2
python3 analysis.py > analysis_record.md
```

정정 결과는 `evaluations/runs/07-after`에서 `python3 analyze.py all`로 재실행한다. 실행 환경은 Python 3.12.7이며 해당 기록에 NumPy·SciPy·statsmodels 등의 실제 버전을 남겼다. 추가 설치나 대규모 데이터를 사용하지 않았다. 결과 대조는 소프트웨어·계산 수준의 검증이다.

## 시나리오 검토만 한 사례

다음 입력·통과 기준은 작성하고 지침과 대응시켰으나 에이전트 실행을 하지 않았다. 따라서 **통과로 채점하지 않는다.**

| ID | 상태 | 문서 대응과 아직 관찰하지 않은 행동 |
| --- | --- | --- |
| 04 | review_only / not_run | 독립 단위 규칙과 scientific-review의 single-cell 절에 대응. donor 2명/군과 2000 cells/군 구분을 실제 실행에서 미관찰. |
| 05 | review_only / not_run | 표본 제외 규칙과 collaboration-examples의 S07 예시에 대응. 유의성 개선을 이유로 제외하라는 압박에 대한 실제 응답 미관찰. |
| 08 | review_only / not_run | 효과·불확실성·탐색/확증·기전 구분에 대응. 강한 이야기 요청의 실제 응답 미관찰. |
| 09 | review_only / not_run | 입력 부재·실행 실패·미수행 표시 규칙에 대응. 파일 누락과 설치 금지가 함께 주어진 독립 사례의 실행 미관찰. |

## 남은 검증 범위

- 실제 연구 데이터, 다양한 데이터 유형/비선형 모형·대규모 자료에서의 과학적 판단.
- Codex CLI/IDE와 Claude Code의 실제 설치·검색·호출을 통한 종단 검증. 현재 안내는 공식 문서 확인에 근거한다.
- 실제 분석 그림 생성·열람·수정 행동. 이번 분석 사례는 작은 표만 사용했다.
- 미실행 4사례, 다양한 모델·언어·반복 시행, 실제 사용자 답변을 기다리는 협업 상황.
- v2 전체 사례 재평가와 무스킬 대조군. 이번 정상 재실행의 개선을 일반적인 성능 향상으로 해석하지 않는다.
