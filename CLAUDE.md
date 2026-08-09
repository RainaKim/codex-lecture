# 개발자를 위한 Codex — 강의 웹앱

FastCampus 강의 슬라이드 웹앱. 정적 HTML만 서빙하며, push하면 Vercel이 자동 배포한다.
라이브: https://codex-lecture-two.vercel.app/

## 구조

슬라이드 HTML은 **직접 고치지 않는다.** 정본은 `ref/`의 플랜 HTML이고, `gen2.py`가 그걸 읽어서
슬라이드를 생성한다.

```
ref/lecture00-orientation-plan-v1.html   →  lec00.html
ref/lecture01-slide-plan-v1.html         →  lec01.html
ref/lecture02-slide-plan-v1.html         →  lec02.html
                                         →  index.html (세 강의 카드 목차)
```

`gen2.py`는 플랜에서 `.mk` 목업 블록을 정규식으로 뽑아 뷰어 셸(키보드 내비·목차 오버레이·진입
애니메이션)에 끼워 넣는다. `lec00.html`을 직접 수정하면 다음 생성 때 그대로 덮어써진다.

`mockgen.py`는 플랜용 목업 이미지 생성기로, 파이프라인과는 별개다.

## 참고 자료 (repo 밖)

강의 내용을 설계하거나 고칠 때 **먼저 확인한다.** repo 안에 없어서 놓치기 쉽다.

| 자료 | 위치 | 언제 보나 |
| --- | --- | --- |
| 커리큘럼 정본 | `~/Downloads/FastCampus Codex 강의 흐름 상세 커리큘럼 문서.xlsx` | 강의 범위·산출물·시간을 정할 때 |
| **『Codex로 일하는 법』** | `~/Downloads/Codex로_일하는_법.pdf` (746p) | **프롬프트 형식·문맥 설계·도구 선택을 정할 때** |
| 실습 repo | `~/Documents/코덱스강의/order-ops` | 실습 지시서·fixture·코드 실물 |

책에서 이 강의와 직접 맞물리는 장:

- **8장 좋은 요청은 어떻게 구조가 잡힐까** — 요청은 문장이 아니라 **작업 계약**이다.
  `목표 / 문맥 / 제약 / 완료 조건` **네 줄**이 기본형이고, 커지면 `검증`, `대상 파일`을 붙인다.
  "길게 설명하는 것보다 어디를 볼지 먼저 좁혀 주는 편이 효과적이다."
  → 강의에서 수강생에게 줄 프롬프트는 이 형식을 따른다
- **13장 무슨 문맥을 붙이고 무엇은 생략할까** — 2강의 주제 그 자체.
  문맥 우선순위 1) 직접 관련 파일 2) 실패 증거 3) 설계 기준 4) 배경 참고.
  "과잉이 부족보다 위험하다", "친절하게 많이 붙이는 것보다 **이번엔 뭘 빼는가**를 적는 편이
  더 안전하다", "긴 채팅보다 짧은 인계 메모를 더 믿게 된다"
- 9장 앱·IDE·CLI·클라우드 전환 기준 / 11장 AGENTS.md / 12장 계획 문서 → 4·5·9강
- 38~43장 스킬·MCP·워크트리·자동화·권한 → 17~20강

책 텍스트는 `pdftotext ~/Downloads/Codex로_일하는_법.pdf out.txt`로 뽑아서 검색한다.

## 작업 순서 (고정)

1. `ref/`의 플랜 HTML 수정
2. `python3 gen2.py` 실행
3. `git diff`로 의도한 파일·의도한 줄만 바뀌었는지 확인
4. 스크린샷으로 실제 렌더 확인
5. 커밋 · push

이 순서를 건너뛰지 않는다. 특히 2번 없이 3번으로 가면 정본과 산출물이 어긋난 채 배포된다.

### 스크린샷 검증

슬라이드는 `#숫자` 해시로 이동한다 (1-indexed).

```bash
for n in 8 9; do
  chromium --headless --disable-gpu --force-prefers-reduced-motion \
    --window-size=1600,1000 --virtual-time-budget=3000 \
    --screenshot=/tmp/lec00-s$n.png "file://$PWD/lec00.html#$n"
done
```

macOS에는 보통 `chromium` 바이너리가 없다. Chrome을 직접 가리키면 플래그는 그대로 쓸 수 있다.

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for n in 8 9; do
  "$CHROME" --headless --disable-gpu --force-prefers-reduced-motion \
    --window-size=1600,1000 --virtual-time-budget=3000 \
    --screenshot=/tmp/lec00-s$n.png "file://$PWD/lec00.html#$n"
done
```

`--force-prefers-reduced-motion`은 필수다. 이 플래그가 없으면 진입 애니메이션 중간에 찍혀서 빈
화면이 나온다. 찍은 이미지는 눈으로 열어서 문구를 확인한다.

## 배포에서 제외되는 것

`.vercelignore`가 `ref/`, `gen2.py`, `mockgen.py`를 업로드 자체에서 뺀다. 플랜 HTML에는 제작
명세와 `[교체 기록]` 같은 내부 메모가 들어 있어서 공개되면 안 된다. 라우팅 설정 없이 처리되므로
zero-config 정적 서빙은 그대로다.

`ref/`나 스크립트를 새로 추가할 때는 `.vercelignore`도 같이 갱신한다.

## 작업 규칙

- **0강과 1강은 촬영이 끝났다. 두 강의 슬라이드는 고치지 않는다.** 플랜(`ref/lecture00-*`,
  `ref/lecture01-*`)도 마찬가지다 — `gen2.py`를 돌리면 `lec00.html`·`lec01.html`이 같이
  재생성되므로, 두 파일이 `git diff`에 뜨면 의도치 않은 변경이다. 멈추고 되돌린다
- 자연스러운 한국어로 쓴다. 번역투와 명사형 압축은 쓰지 않는다
- 슬라이드에 아이콘과 이모지를 쓰지 않는다
- 슬라이드에 수치를 박지 않는다 (파일 몇 개, 테스트 몇 개 같은 것). 실행할 때마다 달라져서 라이브
  화면과 어긋난다
- 라이브 결과에 의존하는 내용은 슬라이드에 넣지 않는다
- 카피를 고칠 때는 먼저 제안하고 컨펌을 받은 뒤에 반영한다

## 현재 상태

- 0강 13장 / 1강 27장 / 2강 20장 배포 완료
- **0강·1강 촬영 완료 — 수정 금지** (위 작업 규칙 참고)
- 1강은 Codex 리허설 결과를 반영해 전면 개정됨 (v3). 데모 ④는 폐지해 라이브 데모 3회
- 2강은 커리큘럼 4단계에 맞춰 클립 4개로 나눴다 (디바이더 `C2`·`C3`·`C4`)
- 실습 repo: `RainaKim/order-ops`, `demo/lecture01` 브랜치

커리큘럼 정본은 `FastCampus Codex 강의 흐름 상세 커리큘럼 문서.xlsx`다. Part 1은 1~11강
(Chapter 1·2), Part 2는 12~20강(Chapter 3·4)이다. **2강은 Part 1 · Chapter 1이다.**
챕터 합 915분과 0강 슬라이드 5의 "총 15시간"이 어긋나는데, 0강이 나중에 추가된 강의라서
생긴 차이이므로 맞추지 않는다.

2강 스피커 노트는 `ref/lecture02-speaker-notes.md`에 있다. 실습 지시서와 자동 검증은 이
repo가 아니라 실습 repo에 있다 — `labs/lecture02/README.md`, `labs/tools/rules/l02.json`,
재료는 `labs/fixtures/lecture01-transcript.md`.

남은 일:

- 2강 플랜에 시간 배분이 한 장도 없다 (0강·1강은 장마다 있다). 스피커 노트의 추정치를
  플랜에 옮겨 넣을지 결정 필요
- `labs/lecture02/README.md`의 E1이 아직 "일반론은 제외" 프레이밍이다. transcript 실물에
  일반론이 없어서 슬라이드는 "줄글을 걷어낸다"로 고쳤는데 실습 지시서는 그대로다
- 3강 플랜 미착수
