# Bioinformatics Analysis Skills

[English](README.md) | [한국어](README.ko.md)

**연구자가 분석을 이해하고 검토하면서 함께 진행할 수 있도록 돕는** 재사용 가능한 Agent Skills입니다. Codex와 Claude Code에서 사용할 수 있습니다.

첫 번째 스킬인 [`bioinformatics-research-assistant`](skills/bioinformatics-research-assistant/SKILL.md)는 데이터를 살펴보고, 과학적 판단을 내리고, 관측 결과를 설명하며, 재실행 가능한 분석을 남기는 방식을 정의합니다.

## 왜 만들었나요?

기존에 접한 생물정보학 스킬 중에는 특정 omics 분석이나 분석 도구를 다루는 데 초점을 맞춘 것이 많았습니다. 저는 그에 더해, 데이터를 탐색하며 측정값의 의미를 이해하고 다음 분석을 결정하는 연구 과정 자체를 돕는 스킬이 필요하다고 느꼈습니다.

Codex나 Claude Code 같은 코딩 에이전트는 작동하는 코드를 빠르게 만들 수 있습니다. 하지만 생물정보학 연구에서는 코드가 실행된다는 사실만으로 충분하지 않습니다. 연구자가 무엇을 했고, 왜 그 방법이 적절하며, 실제로 무엇을 관측했고, 어디까지 해석할 수 있는지 이해할 수 있어야 합니다. 실행에 성공한 코드에도 잘못된 실험 단위, 근거 없는 가정, 자료가 뒷받침하지 않는 생물학적 해석이 숨어 있을 수 있습니다.

이 스킬은 에이전트가 연구자가 따라가고 판단할 수 있는 연구 보조자로 일하도록 만들기 위한 것입니다. 이해할 수 있는 코드와 설명을 작성하고, 의미 있는 과학적 질문 하나씩 분석을 진행하도록 합니다. 데이터를 탐색하고 실제 출력을 확인한 다음, 생물학적·통계적 근거에 따라 다음 분석과 시각화를 선택합니다. 처음 세운 계획은 자료를 확인하면서 수정할 수 있는 잠정적인 계획입니다.

연구자는 중요한 과학적 판단에 참여하고, 에이전트는 이미 합의한 작업과 기본 점검을 불필요한 승인 반복 없이 수행하는 협업을 지향합니다.

탐색적 분석 노트북은 이 목적에 잘 맞습니다. 코드, 출력, 연구자의 해석을 함께 남기면 다른 사람이 읽어도 왜 다음 분석으로 이어졌는지 따라갈 수 있습니다. 그래서 이 스킬은 탐색적 분석에서 실행된 `.ipynb`를 우선 사용합니다. 결과를 확인하면서 노트북을 발전시키고, 관측이 어떤 판단으로 이어졌는지와 결과를 본 뒤 추가한 선택을 함께 기록합니다.

## 어떻게 동작하나요?

의미 있는 질문 하나를 단위로 다음 흐름을 따릅니다.

1. 확인할 질문과 필요한 이유를 설명합니다.
2. 확인된 입력, 잠정 가정, 미확인 사항을 구분합니다.
3. 필요한 최소 분석을 구현하고 실행합니다.
4. 실제 수치·경고와 생성한 그림을 확인합니다.
5. 관측, 해석, 한계를 설명합니다.
6. 그 결과에 근거해 다음 작업을 선택하거나 계획을 수정합니다.

RNA-seq, single-cell, spatial, 유전체 변이, 미생물군집, 생물학적 예측모델이 공유하는 원칙을 다룹니다. 모든 자료에 같은 파이프라인을 강제하지 않습니다. 입력 의미, 독립 반복, 의존성, 혼동, 표본 제외, 불확실성, 데이터 누수, 해석 범위는 해당 상황에 필요한 경우에 확인합니다. 생물정보학과 무관한 웹·앱 개발에는 적용하지 않습니다.

배포되는 스킬 지침은 영어입니다. 사용자와의 대화는 사용자의 언어를 따르며, 언어 선호를 알 수 없으면 한국어를 기본으로 합니다. 계획·검토·스킬 제작만 요청받았다면 임의로 연구 분석을 시작하지 않습니다.

## 노트북으로 분석하기

과학적 질문마다 **질문과 이유 → 코드와 실제 출력 → 관측·해석·한계 → 다음 선택**이 연결되도록 구성합니다. 출력 확인 후 해석을 기록하고, 그 결과에 의존하는 후속 분석을 구현합니다. 중요한 판단은 노트북에도 남겨서 연구자가 대화 기록 없이 분석을 이해할 수 있게 합니다.

노트북을 재현 가능하다고 보고하기 전에는 새 커널에서 순서대로 재실행하고, 새 출력을 확인한 뒤 현재 코드와 함께 저장합니다. 표본 관계가 정정되면 영향을 받는 계산, 출력, 설명을 함께 갱신합니다. 입력 부족, 실행 실패, 검증하지 못한 부분은 분명하게 남깁니다.

탐색적 분석의 기본 방식이며 연구자의 기존 작업 방식을 존중합니다. 기존 분석 문서, 명시적으로 요청한 스크립트, 확립된 파이프라인, 코드 검토, 노트북 실행 환경 부재 등의 상황에서는 다른 형식을 사용할 수 있습니다. 길거나 반복 사용되는 계산은 스크립트로 분리하되 중요한 파라미터, 결과, 선택 이유는 노트북에서 확인할 수 있게 합니다. 노트북만으로 충분하면 별도의 설명 로그나 모든 중간 결과의 개별 파일을 만들지 않습니다.

## 파일 구성

| 파일 | 역할 |
| --- | --- |
| [SKILL.md](skills/bioinformatics-research-assistant/SKILL.md) | 핵심 진행 방식, 과학적 판단, 질문 조건, 보고·완료 기준 |
| [scientific-review.md](skills/bioinformatics-research-assistant/references/scientific-review.md) | 상황별 생물학·통계 검토, 데이터 유형별 주의사항, 확인한 출처 |
| [collaboration-examples.md](skills/bioinformatics-research-assistant/references/collaboration-examples.md) | 설명·질문·정정·한계 전달 예시 |
| [analysis-record.md](skills/bioinformatics-research-assistant/references/analysis-record.md) | 노트북 진행 방식, 저장된 출력과 새 커널 재실행, 간단한 기록과 최종 보고 |
| [평가 입력](evaluations/cases.json)과 [채점 기준](evaluations/rubric.md) | 작은 평가 사례 10개. 입력과 정답 기준은 분리 |
| [평가 보고서](evaluations/REPORT.md) | 실행한 검증, 근거, 수정 이력, 미검증 범위 |
| [노트북 검증](evaluations/NOTEBOOK_WORKFLOW.md) | 새 에이전트의 노트북 행동 검증, 실행 예시, 새 커널 재실행 근거 |

설치 대상은 `skills/bioinformatics-research-assistant/`뿐입니다. 참조 문서는 필요한 경우에만 읽으며, 평가 입력·채점 기준·과거 실행 기록은 배포 스킬 밖에 둡니다. 필수 분석 스크립트, 패키지 설치, 특정 제품 전용 hooks에 의존하지 않습니다.

## 설치

저장소를 복제합니다.

```bash
git clone https://github.com/ilsan142/bioinfo_analysis_skiils.git
cd bioinfo_analysis_skiils
```

아래 위치 중 하나에 **스킬 폴더 전체**를 복사합니다. 같은 제품의 프로젝트·사용자 경로에 서로 다른 복사본이 생기지 않도록 설치 범위를 하나 선택합니다.

| 제품 | 프로젝트 단위 | 사용자 전체 | 명시 호출 |
| --- | --- | --- | --- |
| Codex CLI / IDE | `<project>/.agents/skills/bioinformatics-research-assistant/` | `~/.agents/skills/bioinformatics-research-assistant/` | `$bioinformatics-research-assistant` 또는 `/skills`에서 선택 |
| Claude Code | `<project>/.claude/skills/bioinformatics-research-assistant/` | `~/.claude/skills/bioinformatics-research-assistant/` | `/bioinformatics-research-assistant` |

사용자 전체에 설치하려면 복제한 저장소에서 해당 명령을 실행합니다. 같은 이름의 설치가 이미 있으면 복사를 건너뜁니다. 업데이트할 때는 기존 파일을 먼저 비교합니다.

Codex:

```bash
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/bioinformatics-research-assistant" && \
  test ! -L "$HOME/.agents/skills/bioinformatics-research-assistant" && \
  cp -R skills/bioinformatics-research-assistant "$HOME/.agents/skills/"
```

Claude Code:

```bash
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/bioinformatics-research-assistant" && \
  test ! -L "$HOME/.claude/skills/bioinformatics-research-assistant" && \
  cp -R skills/bioinformatics-research-assistant "$HOME/.claude/skills/"
```

프로젝트 단위 설치는 연구 프로젝트 안의 해당 경로에 복사하면 됩니다. `evaluations/`는 스킬 설치 위치에 복사하지 않습니다. 목록에 나타나지 않으면 스킬 검색 설정을 확인하거나 새 세션을 시작합니다.

설치 위치와 호출법은 2026-10-17에 [Codex 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)를 확인한 내용입니다. 공통 파일은 [Agent Skills 형식](https://agentskills.io/specification)을 따릅니다. 두 제품에서 실제 설치부터 호출까지의 통합 검증은 아직 수행하지 않았습니다.

## 사용 예시

Codex:

```text
$bioinformatics-research-assistant
이 디렉터리의 발현 행렬과 실험 기록을 확인하고 처리 효과 분석을 도와줘.
```

Claude Code:

```text
/bioinformatics-research-assistant 이 디렉터리의 발현 행렬과 실험 기록을 확인하고 처리 효과 분석을 도와줘.
```

생물학적 질문과 현재 제공할 수 있는 데이터·기록을 함께 전달합니다. 에이전트는 기존 정보를 먼저 확인하고 부족한 내용만 질문해야 합니다. 미확인 사항이 일부 분석을 막더라도, 독립적으로 할 수 있는 점검은 계속합니다.

## 검증과 한계

현재 노트북 업데이트는 새 에이전트 두 개에 스킬과 합성 작업 입력만 제공해 검증했습니다. 기대 정답이나 노트북 사용 요청은 전달하지 않았습니다. 둘 다 실행된 노트북을 만들고, 관측을 기록한 뒤 그 결과에 의존하는 분석을 구현했습니다. 정상 사례는 그림을 생성해 실제로 열어 확인했고, 완전 교락 사례는 처리 효과를 분리해 추정할 수 없다고 보고했습니다. 별도의 새 커널 재실행에서도 저장된 출력과 결과표가 재현되었습니다. [검증 기록](evaluations/NOTEBOOK_WORKFLOW.md), [정상 사례 노트북](evaluations/runs/nb-01/analysis.ipynb), [완전 교락 사례 노트북](evaluations/runs/nb-03/treated_control_batch_analysis.ipynb)을 확인할 수 있습니다.

기존 한국어판은 정상 자료, 소수 발현값, 조건·배치의 완전 혼동, 예측 누수, 표본 관계 정정, 무관한 웹 요청의 6종 사례에서 행동을 실행해 관찰했습니다. 작은 산출물을 통합하도록 지침을 보강한 뒤 정상 사례를 재검증했고, 생성된 분석 코드의 별도 프로세스 재실행도 7회 확인했습니다. 나머지 4종은 시나리오 검토만 수행했습니다.

영어판은 별도로 패키지 검사와 새 에이전트를 통한 정상 자료·조건/배치 완전 혼동의 두 사례 재검증을 통과했습니다. 생성된 두 분석을 새 프로세스에서 다시 실행해 결과표가 동일함도 확인했습니다. 나머지 8사례는 번역 후 재실행하지 않았으며, 자세한 범위는 [영어판 검증 기록](evaluations/ENGLISH_EDITION.md)에 남겼습니다. 과거 입력, 스킬 스냅샷, 실행 기록은 근거를 사후에 바꾸지 않도록 원래 언어와 문구를 보존했습니다. 이들은 별도의 설치용 스킬이 아닙니다.

실제 연구 자료, 제품별 통합 동작, 여러 모델에 걸친 신뢰성은 아직 검증하지 않았습니다. 노트북을 쓰지 않는 예외 상황과 기존 노트북의 설계 정정은 이번에 행동 검증을 새로 수행하지 않았습니다. 합성 그림 한 개를 검토한 것이 시각화 전반의 검증을 뜻하지는 않습니다. 합성 자료에서의 실행 성공은 생물학적 검증이 아닙니다.

현재 패키지를 검사하려면 Python 3과 PyYAML이 설치된 환경에서 저장소 루트 기준으로 실행합니다.

```bash
python3 evaluations/validate_package.py
python3 evaluations/prepare_case.py 01 /tmp/bio-skill-case-01-new
```

두 번째 명령은 Python 표준 라이브러리만 사용해 별도 사례 디렉터리를 준비합니다. 에이전트 행동 평가를 실행하는 명령은 아닙니다. 새 에이전트에 그 디렉터리의 스킬과 작업 입력만 제공하고, 실제 행동을 별도의 기준으로 채점합니다. 07번 정정은 초기 결과 뒤에 전달하며, 10번에는 스킬 적용을 강제하지 않고 metadata만 노출합니다.
