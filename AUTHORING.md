# 경험을 계속 추가하는 방법

## 현재 구조에 대한 판단

이전에는 긴 `dist/index.html` 한 파일에 소개, 실무 사례, 프로젝트, 이미지 설명이 함께 들어 있었다. 같은 경험을 여러 위치에서 고치기 쉬워 중복과 이전 표현이 남았고, 일회성 문자열 치환 스크립트를 다시 실행하면 내용이 중복될 위험도 있었다.

현재는 **내용을 개별 HTML 파일에 작성하고, 로컬 조립 스크립트가 전체 페이지를 생성하는 구조**다. 외부 패키지나 런타임 콘텐츠 로딩 없이 Python 표준 라이브러리만 사용한다. 페이지 본문이 처음부터 전체 HTML에 포함되므로 파일로 열기, 이미지 확대, 검색, 인쇄를 유지한다.

## 어디를 수정하나

| 내용 | 수정 위치 |
| --- | --- |
| 첫 소개 | `content/sections/about.html` |
| 전체 이력 타임라인 | `content/sections/journey.html` |
| 회사 경력 요약 | `content/sections/experience.html` |
| 동시성 제어 | `content/cases/approval.html` |
| 운영 로그 정리 | `content/cases/data.html` |
| 고객문의·Jira | `content/cases/jira.html` |
| 원가 정합성 | `content/cases/cost.html` |
| Yesterday’s Trip | `content/projects/trip.html` |
| 여의도꿀통 | `content/projects/honeypot.html` |
| 시작 | `content/projects/perspectiview.html` |
| 기술·연락처 | `content/sections/skills.html`, `contact.html` |
| 섹션·경험 파일 목록과 표시 순서 | `content/site.json` |
| 공통 머리말·푸터·메뉴 | `content/page.html` |

`dist/index.html`은 생성 결과다. 내용을 고칠 때는 해당 `content/` 파일을 수정한다. CSS와 동작은 기존 `dist/*.css`, `dist/script.js`, 이미지는 `dist/assets/`에서 관리한다.

## 새 실무 경험 추가

1. `content/templates/professional.html`을 `content/cases/새경험.html`로 복사한다.
2. 고유한 `id`와 제목, 배경, 담당 범위, 원인, 적용 방식, 확인된 결과를 작성한다. 기존 ID를 바꾸면 링크도 함께 수정해야 한다.
3. `content/site.json`의 `collections.professional.items`에 새 파일 경로를 추가한다.
4. 프로젝트 루트에서 `python build.py`를 실행한다.
5. `python build.py --check`로 조립 결과와 HTML 구조·ID·내부 링크·로컬 이미지 경로를 확인한다.

실무 사례는 상세 본문의 글자 수가 긴 순서로 자동 정렬하고, 표시 번호도 갱신한다. 새 파일만 만들고 목록에 넣지 않으면 공개 페이지에 추가되지 않으므로 초안을 따로 쌓을 수 있다.

## 새 팀·개인 프로젝트 추가

`content/templates/project.html`을 `content/projects/`에 복사하고 `collections.side-projects.items`에 경로를 추가한다. 이 목록은 수동 순서다. 현재는 Yesterday’s Trip → 여의도꿀통 → 시작이다. 기존 세 프로젝트가 팀 프로젝트였다는 사실은 바꾸지 않았다.

## 경험을 작성할 때 남기면 좋은 정보

- **상황:** 누가 어떤 업무를 하다가 문제를 만났는가?
- **원인:** 어떤 시점·조건에서 문제가 생겼고 무엇을 확인했는가?
- **내 역할:** 직접 분석·설계·구현한 범위는 어디까지인가?
- **변경:** 변경 전후의 요청·트랜잭션·데이터 흐름은 무엇이 다른가?
- **결과:** 실제 확인한 동작·수치·검증 근거는 무엇인가?

모르는 날짜·측정값·검증 결과는 만들지 않고 생략하거나 초안 메모에 남긴다. 사례 소개에는 요약과 역할을 쓰고, 본문에는 원인·판단·결과를, 그림 설명에는 그림에서 읽어야 할 요소를 배치해 같은 설명을 반복하지 않는다.

코드보다 흐름을 전달할 때는 기존 `.flowchart`, `.flow-node`, `.flow-decision`, `.flow-branches` 스타일을 재사용한다. 오류 로그 설명과 ‘처리 전에 결재완료로 일괄 변경’ 설명은 사용자가 삭제·정정했으므로 새 경험을 추가하면서 복원하지 않는다. 인덱스 설계 제안 문장도 현재 소개에서 제외했다.

## 한계와 확장 기준

파일을 편집하는 구조이며 웹 관리 화면은 없다. 수십 개 규모의 경험을 하나씩 쌓고 정적 페이지로 검토하기에는 적합하다. 정렬과 최종 조립은 자동화했지만 동일한 경험을 소개와 경력 요약에 언급하면 해당 요약의 문맥은 작성자가 검토해야 한다. 분량이 크게 늘면 목록을 나열하는 한 페이지 외에 분야별 탐색이나 개별 상세 페이지를 검토할 수 있다.

이번 변경에서는 전체 본문을 유지하고 인쇄할 수 있어야 한다는 요구를 우선했다. PDF 파일은 생성하지 않는다.
