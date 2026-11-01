# 유재건 개발자 포트폴리오

전체 본문을 담은 정적 HTML/CSS/JS 사이트입니다. `dist/index.html`을 브라우저로 열면 확인할 수 있으며, 상단 인쇄 버튼 또는 Ctrl+P로 현재 페이지를 PDF로 저장할 수 있습니다. 별도 PDF 파일은 생성하지 않습니다.

## 내용을 수정하고 경험 추가하기

내용의 원본은 `content/`입니다. 자세한 파일 안내와 작성 순서는 [AUTHORING.md](AUTHORING.md)를 참고하세요.

- `content/sections/`: 소개, 전체 이력, 경력, 기술, 연락처.
- `content/cases/`: 실무 사례를 경험별로 분리한 HTML.
- `content/projects/`: Yesterday’s Trip, 여의도꿀통, 시작의 개별 HTML.
- `content/site.json`: 화면 구성과 경험 파일 목록. 실무와 프로젝트 모두 목록 순서로 표시합니다.
- `content/templates/`: 새 경험 작성용 틀. 목록에 등록하기 전에는 페이지에 나오지 않습니다.
- `build.py`: Python 표준 라이브러리만 사용하는 정적 페이지 조립기.

수정 후 프로젝트 폴더에서 `python build.py`를 실행하세요. `python build.py --check`는 HTML 구조·고유 ID·내부 링크·로컬 이미지와 결과 파일의 최신 상태를 검사합니다. `dist/index.html`은 생성 결과이므로 내용을 직접 고치면 다음 조립 시 덮어씁니다. 조립 과정은 네트워크를 사용하지 않습니다.

## 화면과 이미지

- `dist/style.css`: 기본 색상, 레이아웃, 이미지 확대와 인쇄.
- `dist/refinement.css`: 사례·흐름도·모바일·인쇄 조정.
- `dist/journey.css`: 전체 이력 타임라인.
- `dist/script.js`: 테마 전환, 현재 섹션, 이미지 확대와 인쇄 버튼.
- `dist/assets/projects/`: 아키텍처와 설명 이미지.
- `dist/assets/skills/`: 배경이 투명한 기술 SVG 로고.

이미지 추가 시 img의 src와 버튼의 data-full-image 경로를 함께 설정하고, 대체 텍스트와 그림을 읽는 데 필요한 설명을 작성합니다. 전체 상세와 그림 설명은 접기 없이 표시됩니다.

## 출처와 기록

최초 콘텐츠는 제공된 이력서·포트폴리오 PDF에 기반하며 이후 사용자 설명과 정정을 우선해 보완합니다. 원본 PDF는 게시하지 않습니다. 이메일 인증 응답 수치는 당시 프로젝트의 요청 응답 측정값이며 이메일 도착 시간이 아닙니다.

로고는 Devicon(https://github.com/devicons/devicon)과 MyBatis 공식 저장소(https://github.com/mybatis/logo)를 사용하며 권리는 각 소유자에게 있습니다. PDF에서 추출한 기존 PNG는 보존용입니다. 외부 글꼴을 가져오지 못하면 시스템 글꼴을 사용합니다.

변경 이력은 [WORK_LOG.md](WORK_LOG.md), 채용 관점 검토는 [REVIEW.md](REVIEW.md)에 남겼습니다. 기존 일회성 치환 스크립트는 재실행하지 않고 현재 content 파일을 수정합니다. 기존 Sites 프로젝트와 비공개 접근을 유지합니다.

## GitHub Pages

Source: https://github.com/JaegeonYu/developer-portfolio

Website: https://jaegeonyu.github.io/developer-portfolio/

The main branch deploys automatically via .github/workflows/pages.yml. GitHub Actions runs build.py and build.py --check, then publishes only dist/. Existing Sites hosting remains configured separately.
