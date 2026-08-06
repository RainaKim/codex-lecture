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

- 자연스러운 한국어로 쓴다. 번역투와 명사형 압축은 쓰지 않는다
- 슬라이드에 아이콘과 이모지를 쓰지 않는다
- 슬라이드에 수치를 박지 않는다 (파일 몇 개, 테스트 몇 개 같은 것). 실행할 때마다 달라져서 라이브
  화면과 어긋난다
- 라이브 결과에 의존하는 내용은 슬라이드에 넣지 않는다
- 카피를 고칠 때는 먼저 제안하고 컨펌을 받은 뒤에 반영한다

## 현재 상태

- 0강 13장 / 1강 28장 / 2강 17장 배포 완료
- 1강은 Codex 리허설 결과를 반영해 전면 개정됨 (v3)
- 실습 repo: `RainaKim/order-ops`, `demo/lecture01` 브랜치

남은 일:

- 1강 슬라이드 9 톱니 그래프 문구가 v3 논지와 맞는지 점검
- 2강 실습 계획서와 스피커 노트 미작성
- 3강 플랜 미착수
- 커리큘럼 총량 불일치 — 챕터 합 915분 vs 총량 905분
