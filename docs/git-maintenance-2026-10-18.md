# 2026-10-18 Git 정리

- 기존 공개 main과 index.html은 유지한다. 기존 로컬 portfolio.html 초안은 별도 문서 커밋으로 보관했다.
- codex/organize-portfolio에서 초안과 Git 관리/CI를 나누며 기존 커밋 이력을 변경하지 않는다.
- 두 HTML의 로컬 asset 참조 존재와 inline JavaScript 구문을 검사했다. 새 scripts/check_site.py가 같은 검사를 CI에서 수행하며 페이지 코드·외부 링크를 실행하거나 네트워크로 조회하지 않는다.
- 실제 브라우저 레이아웃·접근성·내용 정확성을 이 정적 검사로 확인했다고 주장하지 않는다.
- GitHub Pages/도메인/배포 설정과 기본 페이지는 바꾸지 않는다. 이번 PR은 merge commit으로 초안/관리 커밋을 보존한다.
