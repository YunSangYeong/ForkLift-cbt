# 검증 보고서

확인일: 2026-10-20. 작업 디렉터리: `/workspace/ForkLift-cbt`.

## 적용과 근거

- 원본 앱: `YunSangYeong/electrician-cbt@b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`. 실제 Git archive로 소스·설정·lockfile·테스트·workflow를 가져와 수정했다. 원본의 문항과 생성 스크립트는 새 문제은행으로 대체했다.
- 표준 스킬 v1.2.0의 전체 폴더와 references 5개를 읽고 복사했다. 대상에 없던 AGENTS.md를 만들고 연결했다. 앱 코드 MIT 고지를 보존했다.
- [공식 시험정보 확인 증거](official-rules-evidence.md): Q-Net 지게차운전기능사 코드 7875, HTTP 200. 5개 영역·4지선다·60문항·60분·총점 60점 합격을 확인했다.
- 공식 안내는 과목별 과락 조건을 별도로 제시하지 않는 총점 기준이다. 영역별 12문항과 문항 동일 배점은 학습용 정책이고 공식 분포·문항별 배점표는 미확인이다.
- 공식 출제기준 기간 안내와 보고서 링크는 확인했으나 모든 세부 기준과 문제를 전수 대조하지 않았다. 공식 자료가 각 자체 제작 문제의 정답 근거가 되는 것은 아니다.

## 데이터 인수

| 항목 | 실제 결과 |
| --- | --- |
| 기본 JSON 등록 | 자체 제작 1,000, 기출 0, 복원 0 |
| 학습 영역별 | 주행 200 / 적재 200 / 운반 200 / 하역 200 / 안전관리 200 |
| 구성 | 개념 100 + 계산 30유형 × 30조건 = 900 |
| 기본 내부 검수 / 대기 | 1,000 / 0 (개인 로컬 등록 제외) |
| ID / 정규화 본문·보기 중복 | 0 / 0 |
| 한 회 | 영역별 12문항, 총 60, 고유 ID·family 우선 분산 |
| 계산 검증 | 별도 TypeScript 식·SI 환산 경로로 900개 결과·정답 번호·단위·보기 동치 검사 |
| 내부 문장 검토 | 개념 조건·보기 및 해설, 계산 유형 조건·공식·단위·해설을 검토 |
| 의미상 검토 | 작업 단계별 관련 개념 및 같은 공식의 조건 변형은 의도적으로 존재; 독립 지식 1,000개가 아님 |
| 외부 전문가 검수 | 미실행 |
| 공식 세부 기준 전수 적합성 | 미완료 |

90%가 계산 조건 변형이므로 실제 시험 난이도·출제 유형 비율을 재현하는 문제은행으로 주장하지 않는다. 이론 하중·거리·압력 계산을 실제 운행 허용값으로 사용하지 않는다. [상세 검토 범위](question-review.md).

## 실행 검증

런타임: Node 24.19.0, npm 11.9.0, Python 3.12.14, 시스템 Chromium.

- `npm ci --cache /workspace/.npm-cache --no-audit --no-fund`: 종료 0, lockfile 사용, 의존성 110개 설치.
- `npm run check`: 단위 테스트 920개 통과(900개 계산 문항 포함), TypeScript·production build 통과. 종료 0.
- 브라우저: Playwright, Desktop Chrome / Pixel 7 에뮬레이션, `/usr/bin/chromium`, workers 2. 실기기는 미실행.
- 1차 기존 시나리오 18개 통과. 추가 인수 실행은 22개 통과·2개 실패(통계 화면 안내 요소), 통계 집계 안내를 일반 본문으로 정리한 뒤 해당 2개 재검사 통과. 실패를 통과 수에 섞지 않았다. 최종 전체 실행은 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e`: 24개 통과, 0 실패, 0 건너뜀, 21.6초, 종료 0이다.
- 데이터 생성 반복 시 기본 JSON 바이트 동일성을 확인한다. ID/본문 보기 조합/조건 값 중복과 선택지 유효성도 검사한다.

브라우저 시나리오는 60문항 중 36개 정답→합격·미응답 오답 처리, 답안 변경, 정답 숨김, 제출 취소/확인, 전체 해설/오답 필터, 절대 마감시각 새로고침 복원, 가상시계 60분 만료, 만료 재접속, 타이머 콜백 전 만료 클릭, 제출 중복 방지, 랜덤 연속 정답·즉시 채점, 오답 해제, 북마크·통계, JSON/CSV 등록·중복·원자적 오류·대기·근거 승인·초기화, 두 모드 실제 Space keydown/keyup·포커스·미응답·마지막 문제·컨트롤·메뉴·대화상자 보호를 검증한다.

추가로 각 화면의 상단 상시 안내 배너/기준 선택 UI 부재와 가로 넘침, 저장 쿼터 실패 시 경고·메모리 학습·백업, 손상 원본 보존, 동일 origin iframe의 포커스·Space·저장을 확인한다. 스크린샷으로 PC/모바일 대시보드·문항/해설을 확인한다. 실제 다른 origin 블로그 iframe, 브라우저별 제3자 저장 제한과 실기기는 미실행이다.

대용량 JSON 번들 경고는 남는다(약 1.66MB 비압축, gzip 약 150KB). 앱 구동·테스트·빌드는 통과하나 향후 데이터 분할 로딩을 검토할 수 있다. 경고 한도를 높이거나 검사를 비활성화하지 않았다.

## GitHub·Pages

기본 URL: https://YunSangYeong.github.io/ForkLift-cbt/

저장소의 Git 읽기와 API 읽기는 확인했다. Pages 최초 생성 API는 `403 Resource not accessible by integration`, Pages 조회는 404, 배포 전 공개 URL도 404다. 저장소 관리자 조치: **Settings → Pages → Build and deployment → Source: GitHub Actions**. 환경 네트워크 설정의 문제가 아닌 GitHub integration 권한 범위다.

workflow는 main의 단위·빌드·PC/모바일 검증 성공 후 deploy-pages를 호출한다. 원격 커밋·해당 실행의 CI 및 배포 결과는 아래 실제 확인 후 기록한다. 로컬 성공을 배포 성공으로 표현하지 않는다.

## 재사용 환경 설정

환경 설정 초안에 필요한 도메인 목록 및 `install_script`, `start_skill`을 저장했다. 설치 스크립트는 기존 체크아웃에서 npm ci와 check를 실행하고, 시작 지침은 dev 서버 재시작·준비 확인·브라우저 검사·Pages 경로를 안내한다. 비밀값은 불필요하다. 초안 저장은 실행이나 게시와 다르며 사용자 환경 설정 검토·저장 및 Publish는 별도 단계다. 새 클라우드 작업에서의 복원은 검증하지 않았다.

## 실제 원격 실행 증거

앱 구현 커밋: `d24b6f9ff17fa74f5bcfee2052a4453a37d026b0` (main push 및 원격 SHA 확인).

실행: https://github.com/YunSangYeong/ForkLift-cbt/actions/runs/39361316488

- `validate`: 성공. npm ci, 920개 단위 검사, Chromium 설치, TypeScript·production build 및 24개 PC/모바일 브라우저 검사, Pages 아티팩트 업로드가 완료됐다.
- `deploy`: 실패. `actions/configure-pages@v5`가 Pages 조회에서 `HttpError: Not Found`를 받았다. `deploy-pages` 단계는 실행되지 않았다.
- check-run annotation은 Pages 활성화와 GitHub Actions Source 설정을 요구한다. 공식 `configure-pages@v5/action.yml`의 enablement 설명은 GITHUB_TOKEN 이외의 토큰과 GitHub App의 `administration:write` 및 `pages:write`를 요구한다. 현재 통합 인증의 직접 생성은 403이므로 무작정 enablement를 켜거나 토큰을 코드에 넣지 않았다.
- 공개 주소는 배포 전 404를 확인했다. 공개 앱 기능 검증은 게시가 완료되지 않아 차단 상태다. 배포 성공으로 보고하지 않는다.
- 관리자 설정 후 Actions에서 실패한 최신 실행을 다시 실행하면 된다. 설정 변경 뒤에는 최신 커밋의 deploy 성공과 공개 주소에서 학습 시작·답안·해설·Space·저장 동작을 다시 확인해야 한다.

후속 정리는 CSV 양식의 줄바꿈을 LF로 고정하고 Space의 IME·수정키·반복 이벤트 보호 검사를 확장했다. 재생성 관련 단위 1개 통과(필터 밖 919개는 건너뜀), PC/모바일 CSV·Space 관련 4개 통과, 종료 0. 앱·문항 내용은 바꾸지 않았다. 개발 서버도 `npm run dev -- --port 5173 --strictPort`로 시작하고 실제 브라우저에서 랜덤 학습 시작→답안 선택→해설 표시를 확인했다. 최종 커밋의 상태는 저장소 Actions에서 해당 SHA와 함께 확인할 수 있다.
