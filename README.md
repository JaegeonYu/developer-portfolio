# 유재건 개발자 포트폴리오

지금까지의 진행 과정과 다음 작업은 [WORK_LOG.md](WORK_LOG.md)에 기록했습니다.

`dist/index.html`을 브라우저로 열면 볼 수 있습니다. 빌드나 설치가 필요 없습니다.

- `dist/index.html`: 소개, 엠로 경력, 실무 사례 4개, 취업 전 프로젝트 3개, 기술, 학습 이력, 연락처.
- `dist/style.css`: 색상, 타이포그래피, 반응형 레이아웃. 맨 위 CSS 변수로 주요 색상을 바꿀 수 있습니다.
- `dist/script.js`: 테마 전환, 현재 섹션 표시.

프로젝트 상세는 접기 없이 본문에 모두 표시됩니다. 카드의 그래픽은 수치와 주제를 시각화한 것으로 실제 서비스 화면이 아닙니다.

## 이미지 교체 및 추가

취업 전 프로젝트 카드에는 PDF에서 추출한 아키텍처를 넣었습니다. 상세 안에서는 쿼리 분리, 배포 자동화, 방화벽과 프록시 변경 다이어그램도 볼 수 있습니다. 이미지를 누르면 확대 창이 열리며 닫기 버튼, Escape 또는 창 밖 클릭으로 닫을 수 있습니다.

- 프로젝트 이미지: `dist/assets/projects/`. HTML의 `img src`와 버튼의 `data-full-image`를 같은 파일 경로로 설정합니다. `alt`, `data-caption`, 이미지 크기도 함께 수정합니다.
- 회사 프로젝트에도 기존 `case-art` 영역 대신 다른 카드의 `project-cover` 버튼 구조를 복사해 이미지를 넣을 수 있습니다.
- 스킬 이미지: `dist/assets/skills/`. 기술 카드는 `skill-card`의 이미지 경로와 이름, 활용 설명을 수정합니다.
- PDF 이미지와 Java/Spring/MyBatis/Docker/MySQL/AWS/Jenkins 로고는 제공된 포트폴리오에서 추출했습니다. Oracle 로고는 Devicon의 `icons/oracle/oracle-original.svg`를 사용했습니다(https://github.com/devicons/devicon). 브랜드 로고의 권리는 각 소유자에게 있습니다.

이메일, GitHub, 기술 블로그 링크를 연결했습니다. 외부 글꼴을 불러오지 못할 때는 시스템 산세리프 글꼴로 표시됩니다.

내용 출처는 사용자가 제공한 `유재건_261031.pdf`와 `유재건_main_포트폴리오_ (2).pdf`입니다. 서로 다른 내용은 최신 이력서를 우선했습니다. Yesterday’s Trip의 응답 시간은 과거 프로젝트 자료의 당시 측정값으로 표시했습니다. PDF 원본은 게시 파일에 포함하지 않았습니다.

구성 참고: https://min-hyuk.com/ 및 https://cdg-portfolio.com/ . 원본의 개인 정보나 프로젝트 내용은 사용하지 않았습니다.

현재 프로젝트 상세는 모두 본문에 표시됩니다. 상단 ‘PDF로 저장 / 인쇄’ 버튼 또는 Ctrl+P로 전체 내용을 A4 PDF로 저장할 수 있습니다. 인쇄 시 한 열 구성과 밝은 색상을 적용하며, 각 이미지 아래의 설명도 포함합니다. 기본 출력 파일은 dist/portfolio.pdf입니다.

## 현재 구성과 로고 출처

화면 순서는 대표 경험 요약 → 경력 → 실무 사례 → 기술 → 팀 프로젝트 → 일하는 방식 → 학습 → 연락처입니다. `dist/refinement.css`에서 최신 화면·인쇄 조정을 관리합니다. `REVIEW.md`에 채용 관점 검토와 추가로 확인해야 할 근거를 정리했습니다.

현재 기술 로고는 투명 SVG입니다. Java·Spring·Docker·MySQL·AWS·Jenkins·Oracle은 https://github.com/devicons/devicon , MyBatis는 https://github.com/mybatis/logo 에서 가져왔습니다. 기존 PDF 추출 PNG는 보존용이며 현재 페이지에서 사용하지 않습니다. 로고의 권리는 각 소유자에게 있습니다.
