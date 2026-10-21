# Bioinformatics Analysis Skills

[English](README.md) | [한국어](README.ko.md)

**연구자가 분석을 이해하고 검토하면서 함께 진행할 수 있도록 돕는** 재사용 가능한 Agent Skills입니다. Codex와 Claude Code에서 사용할 수 있습니다.

| 스킬 | 사용할 때 | 주요 산출물 |
| --- | --- | --- |
| [`bioinformatics-analysis-planner`](skills/bioinformatics-analysis-planner/SKILL.md) | 데이터와 실험 기록을 바탕으로 질문·비교·방법·우선순위를 설계하거나 기존 설계를 크게 수정할 때 | 확인된 근거, 조건별 선택, 첫 실행 단계가 담긴 분석 설계 |
| [`bioinformatics-research-assistant`](skills/bioinformatics-research-assistant/SKILL.md) | 데이터를 탐색하고 실제 분석을 실행·검토·해석할 때 | 질문과 실제 출력, 해석, 다음 판단이 연결된 재실행 가능한 분석 |
| [`bioinformatics-lab-meeting-assistant`](skills/bioinformatics-lab-meeting-assistant/SKILL.md) | 기존 결과나 계획으로 연구 진행 상황과 설계 방향을 논의할 때 | 청중에 맞는 발표 구성, 발표 노트, 근거 위치와 논의할 결정 |
| [`scientific-figure-reviewer`](skills/scientific-figure-reviewer/SKILL.md) | 과학적 그림·캡션이 근거와 실험 설계를 정확히 전달하는지 검토할 때 | 문제 위치, 해석에 미치는 영향, 우선순위와 구체적인 수정안 |
| [`bioinformatics-manuscript-assistant`](skills/bioinformatics-manuscript-assistant/SKILL.md) | 실제 결과와 방법 기록으로 요청한 논문 부분을 작성·수정할 때 | 근거와 연결된 초안, 해석 범위, 확인이 필요한 방법 정보 |

각 스킬은 독립적으로 사용할 수 있습니다. 별도 설계가 필요하면 planner로 방향을 정하고 research assistant가 실행하며 갱신합니다. 랩미팅 구성·그림 검토·논문 초안은 해당 산출물이 필요할 때 요청합니다. 다섯 스킬을 순서대로 적용할 의무는 없으며, 설명이나 글쓰기 요청만으로 새 분석을 시작하지 않습니다.

## 왜 만들었나요?

기존에 접한 생물정보학 스킬 중에는 특정 omics 분석이나 분석 도구를 다루는 데 초점을 맞춘 것이 많았습니다. 저는 그에 더해, 데이터를 탐색하며 측정값의 의미를 이해하고 다음 분석을 결정하는 연구 과정 자체를 돕는 스킬이 필요하다고 느꼈습니다.

Codex나 Claude Code 같은 코딩 에이전트는 작동하는 코드를 빠르게 만들 수 있습니다. 하지만 생물정보학 연구에서는 코드가 실행된다는 사실만으로 충분하지 않습니다. 연구자가 무엇을 했고, 왜 그 방법이 적절하며, 실제로 무엇을 관측했고, 어디까지 해석할 수 있는지 이해할 수 있어야 합니다. 실행에 성공한 코드에도 잘못된 실험 단위, 근거 없는 가정, 자료가 뒷받침하지 않는 생물학적 해석이 숨어 있을 수 있습니다.

이 스킬은 에이전트가 연구자가 따라가고 판단할 수 있는 연구 보조자로 일하도록 만들기 위한 것입니다. 이해할 수 있는 코드와 설명을 작성하고, 의미 있는 과학적 질문 하나씩 분석을 진행하도록 합니다. 데이터를 탐색하고 실제 출력을 확인한 다음, 생물학적·통계적 근거에 따라 다음 분석과 시각화를 선택합니다. 처음 세운 계획은 자료를 확인하면서 수정할 수 있는 잠정적인 계획입니다.

연구자는 중요한 과학적 판단에 참여하고, 에이전트는 이미 합의한 작업과 기본 점검을 불필요한 승인 반복 없이 수행하는 협업을 지향합니다.

탐색적 분석 노트북은 이 목적에 잘 맞습니다. 코드, 출력, 연구자의 해석을 함께 남기면 다른 사람이 읽어도 왜 다음 분석으로 이어졌는지 따라갈 수 있습니다. 그래서 이 스킬은 탐색적 분석에서 실행된 `.ipynb`를 우선 사용합니다. 결과를 확인하면서 노트북을 발전시키고, 관측이 어떤 판단으로 이어졌는지와 결과를 본 뒤 추가한 선택을 함께 기록합니다.

## Research assistant는 어떻게 분석하나요?

분석 실행을 요청받으면 의미 있는 질문 하나를 단위로 다음 흐름을 따릅니다.

1. 확인할 질문과 필요한 이유를 설명합니다.
2. 확인된 입력, 잠정 가정, 미확인 사항을 구분합니다.
3. 필요한 최소 분석을 구현하고 실행합니다.
4. 실제 수치·경고와 생성한 그림을 확인합니다.
5. 관측, 해석, 한계를 설명합니다.
6. 그 결과에 근거해 다음 작업을 선택하거나 계획을 수정합니다.

RNA-seq, single-cell, spatial, 유전체 변이, 미생물군집, 생물학적 예측모델이 공유하는 원칙을 다룹니다. 모든 자료에 같은 파이프라인을 강제하지 않습니다. 입력 의미, 독립 반복, 의존성, 혼동, 표본 제외, 불확실성, 데이터 누수, 해석 범위는 해당 상황에 필요한 경우에 확인합니다. 생물정보학과 무관한 웹·앱 개발에는 적용하지 않습니다.

배포되는 스킬 지침은 영어입니다. 사용자와의 대화는 사용자의 언어를 따르며, 언어 선호를 알 수 없으면 한국어를 기본으로 합니다. 계획·검토·스킬 제작만 요청받았다면 임의로 연구 분석을 시작하지 않습니다.

## 데이터에서 분석 설계 만들기

`bioinformatics-analysis-planner`는 데이터 의미, 독립적인 실험 단위, 가능한 비교를 확인하는 가벼운 점검부터 시작합니다. 연구 질문과 관심 있는 효과를 정리한 뒤 권장 방법의 근거, 필요한 전제, 어떤 결과에서 방법을 바꾸거나 추론을 보류할지를 설계에 남깁니다. 산출물은 기존 분석 기록의 계획 부분 또는 간결한 `analysis_plan.md`입니다.

설계만 요청받았다면 차등발현·전체 군집화·예측모델 학습까지 진행하지 않습니다. 이미 설계와 실행을 함께 요청했다면 불필요한 재승인 없이 분석을 이어갑니다. 계획은 잠정적이며, 실제 결과를 본 뒤 바꾼 선택과 그 이유를 기록합니다.

모델 성능과 별개로, 이 역할 분리는 연구자의 의도와 분석 판단을 명시적으로 남기기 위한 설계입니다. 스킬을 추가했다고 과학적 정확성이나 모델 성능이 향상됐다고 보장하지는 않습니다. 간단한 분석은 기존 research assistant만으로도 설계와 실행을 함께 진행할 수 있습니다.

## 노트북으로 분석하기

과학적 질문마다 **질문과 이유 → 코드와 실제 출력 → 관측·해석·한계 → 다음 선택**이 연결되도록 구성합니다. 출력 확인 후 해석을 기록하고, 그 결과에 의존하는 후속 분석을 구현합니다. 중요한 판단은 노트북에도 남겨서 연구자가 대화 기록 없이 분석을 이해할 수 있게 합니다.

노트북을 재현 가능하다고 보고하기 전에는 새 커널에서 순서대로 재실행하고, 새 출력을 확인한 뒤 현재 코드와 함께 저장합니다. 표본 관계가 정정되면 영향을 받는 계산, 출력, 설명을 함께 갱신합니다. 입력 부족, 실행 실패, 검증하지 못한 부분은 분명하게 남깁니다.

탐색적 분석의 기본 방식이며 연구자의 기존 작업 방식을 존중합니다. 기존 분석 문서, 명시적으로 요청한 스크립트, 확립된 파이프라인, 코드 검토, 노트북 실행 환경 부재 등의 상황에서는 다른 형식을 사용할 수 있습니다. 길거나 반복 사용되는 계산은 스크립트로 분리하되 중요한 파라미터, 결과, 선택 이유는 노트북에서 확인할 수 있게 합니다. 노트북만으로 충분하면 별도의 설명 로그나 모든 중간 결과의 개별 파일을 만들지 않습니다.

## 연구 판단을 돕는 설명

분석 스킬은 낯선 출력을 보여주기 전에 읽는 방법을 안내하고, 실제 관측을 확인한 뒤 남은 불확실성과 다음 점검의 이유를 연결합니다. 설계 스킬은 서로 다른 결과나 판단 불가능한 결과에서 선택이 어떻게 달라지는지 설명합니다. 결과를 본 뒤 발견을 기록하며, 원하는 이야기 때문에 결과를 정하지 않습니다.

새 스킬은 기존 근거를 활용합니다. 랩미팅 스킬은 질문·실제 결과·논의할 결정을 연결합니다. 그림 검토는 눈으로 확인한 문제, 원자료 대조, 아직 확인할 수 없는 사항을 구분합니다. 논문 작성은 정정된 현재 결과와 실행 기록을 사용하며, 부족한 방법 정보를 그럴듯한 내용으로 채우지 않습니다.

탐색 노트북에는 중요한 선택, 반대 증거, 사후 변경을 보존합니다. 이후 발표에서 설명 순서를 바꾸더라도 그 사실과 원래 근거의 연결은 유지합니다. 결론을 바꿀 수 있는 한계를 설명 간소화를 이유로 숨기지 않습니다.

이 보강은 [MIT BE CommKit](https://mitcommlab.mit.edu/be/use-the-commkit/)과 [Broad CommKit](https://mitcommlab.mit.edu/broad/use-the-commkit/)을 참고했습니다. 각 참조 파일에 2026-10-21에 확인한 구체적인 페이지를 표시했습니다. 이 자료는 설명 방식의 참고 자료이며 통계 방법 검증이나 스킬에 대한 기관의 보증은 아닙니다. 일부 Broad 문서는 BE 자료를 바탕으로 하므로 독립적인 과학적 근거로 중복 계산하지 않습니다. 지침과 예시는 새로 작성했으며 원문 구절이나 그림을 복제하지 않았습니다. 원문 사이트는 별도 표시가 없는 콘텐츠에 CC BY-NC 4.0을 명시합니다.

다섯 스킬 다음으로 검토할 후보는 [확장 계획](docs/ROADMAP.md)에 정리했습니다. 아직 구현된 기능은 아닙니다.

## 파일 구성

| 파일 | 역할 |
| --- | --- |
| [Planner SKILL.md](skills/bioinformatics-analysis-planner/SKILL.md) | 질문·자료·설계 타당성·조건별 선택·실행 범위·인계 기준 |
| [설계 문서 지침](skills/bioinformatics-analysis-planner/references/analysis-plan.md) | 간결한 설계 형식과 상황별 분기 예시 |
| [Research assistant SKILL.md](skills/bioinformatics-research-assistant/SKILL.md) | 핵심 진행 방식, 과학적 판단, 질문 조건, 보고·완료 기준 |
| [scientific-review.md](skills/bioinformatics-research-assistant/references/scientific-review.md) | 상황별 생물학·통계 검토, 데이터 유형별 주의사항, 확인한 출처 |
| [collaboration-examples.md](skills/bioinformatics-research-assistant/references/collaboration-examples.md) | 설명·질문·정정·한계 전달 예시 |
| [analysis-record.md](skills/bioinformatics-research-assistant/references/analysis-record.md) | 노트북 진행 방식, 저장된 출력과 새 커널 재실행, 간단한 기록과 최종 보고 |
| [랩미팅 스킬](skills/bioinformatics-lab-meeting-assistant/SKILL.md)과 [예시](skills/bioinformatics-lab-meeting-assistant/references/storyboard-example.md) | 근거 선택, 발표 노트, 시간 배분, 논의할 결정 |
| [그림 검토 스킬](skills/scientific-figure-reviewer/SKILL.md)과 [예시](skills/scientific-figure-reviewer/references/review-examples.md) | 실제 시각적 검토, 원자료 확인과 구체적 수정안 |
| [논문 작성 스킬](skills/bioinformatics-manuscript-assistant/SKILL.md)과 [참고 자료](skills/bioinformatics-manuscript-assistant/references/writing-sources.md) | 요청한 부분 작성, 충돌하는 기록 처리와 해석 범위 |
| [평가 입력](evaluations/cases.json)과 [채점 기준](evaluations/rubric.md) | 작은 평가 사례 10개. 입력과 정답 기준은 분리 |
| [평가 보고서](evaluations/REPORT.md) | 실행한 검증, 근거, 수정 이력, 미검증 범위 |
| [노트북 검증](evaluations/NOTEBOOK_WORKFLOW.md) | 새 에이전트의 노트북 행동 검증, 실행 예시, 새 커널 재실행 근거 |

설치 대상은 `skills/` 아래에서 선택한 스킬 폴더입니다. planner 검증 범위는 [별도 기록](evaluations/planner/REPORT.md)에 있습니다. 참조 문서는 필요한 경우에만 읽으며, 평가 입력·채점 기준·과거 실행 기록은 배포 스킬 밖에 둡니다. 필수 분석 스크립트, 패키지 설치, 특정 제품 전용 hooks에 의존하지 않습니다.

## 설치

저장소를 복제합니다.

```bash
git clone https://github.com/ilsan142/bioinfo_analysis_skiils.git
cd bioinfo_analysis_skiils
```

아래 위치 중 하나에 **선택한 스킬 폴더 전체**를 복사합니다. `<skill-name>`에는 위 표의 실제 스킬 이름을 넣습니다. 같은 제품의 프로젝트·사용자 경로에 서로 다른 복사본이 생기지 않도록 설치 범위를 하나 선택합니다.

| 제품 | 프로젝트 단위 | 사용자 전체 | 명시 호출 |
| --- | --- | --- | --- |
| Codex CLI / IDE | `<project>/.agents/skills/<skill-name>/` | `~/.agents/skills/<skill-name>/` | `$<skill-name>` 또는 `/skills`에서 선택 |
| Claude Code | `<project>/.claude/skills/<skill-name>/` | `~/.claude/skills/<skill-name>/` | `/<skill-name>` |

사용자 전체에 설치하려면 복제한 저장소에서 해당 명령을 실행합니다. `skill_name`을 설치할 이름으로 설정하며, 원하는 스킬마다 이름을 바꾸어 실행합니다. 같은 이름의 설치가 이미 있으면 복사를 건너뜁니다. 업데이트할 때는 기존 파일을 먼저 비교합니다.

Codex:

```bash
skill_name=bioinformatics-analysis-planner
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/$skill_name" && \
  test ! -L "$HOME/.agents/skills/$skill_name" && \
  cp -R "skills/$skill_name" "$HOME/.agents/skills/"
```

Claude Code:

```bash
skill_name=bioinformatics-analysis-planner
mkdir -p "$HOME/.claude/skills"
test ! -e "$HOME/.claude/skills/$skill_name" && \
  test ! -L "$HOME/.claude/skills/$skill_name" && \
  cp -R "skills/$skill_name" "$HOME/.claude/skills/"
```

프로젝트 단위 설치는 연구 프로젝트 안의 해당 경로에 복사하면 됩니다. `evaluations/`는 스킬 설치 위치에 복사하지 않습니다. 목록에 나타나지 않으면 스킬 검색 설정을 확인하거나 새 세션을 시작합니다.

설치 위치와 호출법은 2026-10-19에 [Codex 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)를 확인한 내용입니다. 공통 파일은 [Agent Skills 형식](https://agentskills.io/specification)을 따릅니다. 두 제품에서 실제 설치부터 호출까지의 통합 검증은 아직 수행하지 않았습니다.

## 사용 예시

설계가 필요할 때는 다음처럼 호출합니다. 분석 실행은 별도 요청하거나, 처음부터 설계와 실행을 함께 요청할 수 있습니다.

Codex:

```text
$bioinformatics-analysis-planner
이 디렉터리의 데이터와 실험 기록을 확인하고 처리 효과를 분석할 설계만 작성해줘. 필요한 가벼운 점검을 수행하고, 판단이 필요한 사항과 첫 실행 단계를 남겨줘.
```

Claude Code:

```text
/bioinformatics-analysis-planner 이 디렉터리의 데이터와 실험 기록을 확인하고 분석 설계를 작성해줘.
```

설계에 따라 실행할 때:

```text
$bioinformatics-research-assistant
analysis_plan.md를 읽고 첫 미완료 단계부터 실행해줘. 각 결과를 확인한 뒤 다음 단계를 선택하고 필요한 설계 변경을 기록해줘.
```

아래는 별도 계획 문서 없이 바로 분석하는 예시입니다.

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

설명·검토 작업은 필요한 산출물을 명시해 호출할 수 있습니다.

```text
$bioinformatics-lab-meeting-assistant
analysis.ipynb와 기존 출력으로 10분 랩미팅을 준비해줘. 청중은 single-cell 분석에 익숙하지 않은 생물학 연구자야. 발표 노트와 다음 실험에 관해 논의할 질문을 포함하고 새 분석은 하지 마.

$scientific-figure-reviewer
논문용 figure1.png, 캡션, donor_summary.csv를 검토해줘. 해석에 영향을 주는 문제부터 수정안을 제시하되 원본 파일은 바꾸지 마.

$bioinformatics-manuscript-assistant
정정된 결과표와 실행 기록으로 Results와 Methods를 작성해줘. 확인할 수 없는 방법 정보는 표시하고 이전 결과와 현재 결과를 구분해줘.
```

Claude Code에서는 같은 스킬 이름 앞의 `$`를 `/`로 바꿉니다. 다른 스킬을 함께 설치할 필요는 없습니다.

## 검증과 한계

이번 설명·글쓰기 보강의 [검증 기록](evaluations/communication/REPORT.md), [작업 입력 네 가지](evaluations/communication/cases.json)(새 스킬 세 가지와 검토 범위 회귀 시험), [채점 기준](evaluations/communication/rubric.md)은 별도로 관리합니다. 추가 상황별 사례는 실행했다고 명시하기 전까지 평가 설계입니다. 기록에서 패키지 검사, 정답을 주지 않은 에이전트 수행, 산출물 검토, 미검증 범위를 구분합니다.

Planner 최초 배포에서는 패키지 검사와 합성 자료 3종의 실제 입력 점검, 작성자 설계 예시를 확인했으며 독립 에이전트 행동 검증은 없었습니다. 당시 범위는 [Planner 최초 검증 기록](evaluations/planner/REPORT.md)에 보존했습니다. 이번 업데이트의 새 에이전트 검증과 한계는 위의 설명·글쓰기 검증 기록에 남깁니다. 아래 과거 검증은 research assistant에 해당합니다.

앞선 노트북 업데이트는 새 에이전트 두 개에 스킬과 합성 작업 입력만 제공해 검증했습니다. 기대 정답이나 노트북 사용 요청은 전달하지 않았습니다. 둘 다 실행된 노트북을 만들고, 관측을 기록한 뒤 그 결과에 의존하는 분석을 구현했습니다. 정상 사례는 그림을 생성해 실제로 열어 확인했고, 완전 교락 사례는 처리 효과를 분리해 추정할 수 없다고 보고했습니다. 별도의 새 커널 재실행에서도 저장된 출력과 결과표가 재현되었습니다. [검증 기록](evaluations/NOTEBOOK_WORKFLOW.md), [정상 사례 노트북](evaluations/runs/nb-01/analysis.ipynb), [완전 교락 사례 노트북](evaluations/runs/nb-03/treated_control_batch_analysis.ipynb)을 확인할 수 있습니다.

기존 한국어판은 정상 자료, 소수 발현값, 조건·배치의 완전 혼동, 예측 누수, 표본 관계 정정, 무관한 웹 요청의 6종 사례에서 행동을 실행해 관찰했습니다. 작은 산출물을 통합하도록 지침을 보강한 뒤 정상 사례를 재검증했고, 생성된 분석 코드의 별도 프로세스 재실행도 7회 확인했습니다. 나머지 4종은 시나리오 검토만 수행했습니다.

영어판은 별도로 패키지 검사와 새 에이전트를 통한 정상 자료·조건/배치 완전 혼동의 두 사례 재검증을 통과했습니다. 생성된 두 분석을 새 프로세스에서 다시 실행해 결과표가 동일함도 확인했습니다. 나머지 8사례는 번역 후 재실행하지 않았으며, 자세한 범위는 [영어판 검증 기록](evaluations/ENGLISH_EDITION.md)에 남겼습니다. 과거 입력, 스킬 스냅샷, 실행 기록은 근거를 사후에 바꾸지 않도록 원래 언어와 문구를 보존했습니다. 이들은 별도의 설치용 스킬이 아닙니다.

이 저장소에 공개한 평가 근거는 합성 사례입니다. 제품별 통합 동작과 여러 모델에 걸친 신뢰성은 아직 검증하지 않았습니다. 노트북을 쓰지 않는 예외 상황과 기존 노트북의 설계 정정은 이번에 행동 검증을 새로 수행하지 않았습니다. 합성 그림 한 개를 검토한 것이 시각화 전반의 검증을 뜻하지는 않습니다. 합성 자료에서의 실행 성공은 생물학적 검증이 아닙니다.

현재 패키지를 검사하려면 Python 3과 PyYAML이 설치된 환경에서 저장소 루트 기준으로 실행합니다.

```bash
python3 evaluations/validate_package.py
python3 evaluations/prepare_case.py 01 /tmp/bio-skill-case-01-new
python3 evaluations/prepare_case.py 01 /tmp/bio-planner-case-01-new --suite planner
python3 evaluations/prepare_case.py 02 /tmp/bio-figure-case-02-new --suite communication
```

`prepare_case.py` 명령은 Python 표준 라이브러리만 사용해 별도 사례 디렉터리를 준비합니다. 에이전트 행동 평가를 실행하는 명령은 아닙니다. 새 에이전트에 그 디렉터리의 스킬과 작업 입력만 제공하고, 실제 행동을 별도의 기준으로 채점합니다. 07번 정정은 초기 결과 뒤에 전달하며, 10번에는 스킬 적용을 강제하지 않고 metadata만 노출합니다.
