# -*- coding: utf-8 -*-
"""데모 캡처 목업 3종 생성 — Codex 챗 UI 스타일 (계획서 기대 답변 그대로)"""
import os, subprocess

CSS = '''
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:"Pretendard",-apple-system,"Apple SD Gothic Neo",sans-serif;background:#ECECF1;width:1440px;height:505px;overflow:hidden;}
.win{position:absolute;inset:0;background:#fff;display:flex;flex-direction:column;}
.bar{height:44px;background:#F7F7F8;border-bottom:1px solid #E5E5EA;display:flex;align-items:center;padding:0 16px;flex:none;}
.dot{width:12px;height:12px;border-radius:50%;margin-right:8px;}
.title{margin-left:12px;font-size:15px;color:#6E6E80;font-weight:600;}
.body{flex:1;padding:20px 40px;overflow:hidden;}
.u{display:flex;justify-content:flex-end;margin-bottom:16px;}
.u .b{background:#F1F1F4;border-radius:16px;padding:10px 18px;font-size:17px;color:#202123;max-width:75%;}
.u .b .att{display:inline-block;background:#E3E3EA;border-radius:8px;padding:2px 10px;font-size:14px;color:#6E6E80;margin-left:8px;}
.a{display:flex;gap:14px;}
.logo{width:30px;height:30px;border-radius:8px;background:#0F0F14;color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;flex:none;margin-top:2px;}
.msg{font-size:16.5px;line-height:1.62;color:#202123;max-width:88%;}
.msg p{margin-bottom:8px;}
.msg ol{margin:2px 0 8px 22px;}
.msg ol li{margin:3px 0;}
.msg .mono{font-family:"SF Mono",ui-monospace,Menlo,monospace;font-size:15px;background:#F4F4F6;border-radius:5px;padding:1px 7px;color:#374151;}
.msg .hl{background:#FFE5EB;border-radius:5px;padding:1px 7px;color:#C4103C;font-weight:700;font-family:"SF Mono",ui-monospace,Menlo,monospace;font-size:15px;}
.msg .gray{color:#8E8EA0;font-size:15px;}
.chip{display:inline-block;background:#F4F4F6;border:1px solid #E5E5EA;border-radius:8px;padding:3px 12px;font-size:14px;color:#565869;margin:2px 6px 2px 0;font-family:ui-monospace,Menlo,monospace;}
'''

HEAD = '''<div class="bar"><span class="dot" style="background:#FF5F57"></span><span class="dot" style="background:#FEBC2E"></span><span class="dot" style="background:#28C840"></span><span class="title">Codex — order-ops</span></div>'''

def page(user, attach, answer):
    att = f'<span class="att">{attach}</span>' if attach else ''
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>{CSS}</style></head><body><div class="win">{HEAD}
<div class="body">
<div class="u"><div class="b">{user}{att}</div></div>
<div class="a"><div class="logo">◎</div><div class="msg">{answer}</div></div>
</div></div></body></html>'''

MOCKS = {
  # 데모 ① — 설명 없이: 일반론, 파일명 0개
  'mock-noctx': page('주문 상태 처리 개선해줘', None, '''
<p>주문 상태 관리를 개선하는 일반적인 방법을 제안드릴게요.</p>
<ol>
<li>상태 값을 <span class="mono">enum</span>으로 정의해 문자열 하드코딩을 제거하세요</li>
<li>상태 전이는 <b>상태 머신 패턴</b>으로 관리하는 것이 안전합니다</li>
<li>실패 케이스에 대한 에러 핸들링과 로깅을 추가하는 것을 권장합니다</li>
</ol>
<p class="gray">프로젝트 구조를 공유해 주시면 더 구체적으로 도와드릴 수 있어요.</p>'''),

  # 데모 ① 세션 A — 컨텍스트 붙여서: payments.ts:88 + 정책 3개
  'mock-ctx': page('주문 상태 처리 개선해줘', '1,500자 컨텍스트 · 상태 5개 · 정책 3줄 · 완료 조건', '''
<p><span class="mono">order-ops</span> 구조 기준으로 수정 지점을 정리했어요.</p>
<ol>
<li><span class="hl">payments.ts:88</span> — 결제 실패 시 주문을 삭제하지 말고 <span class="mono">payment_failed</span>로 보존 <span class="gray">(정책 ②)</span></li>
<li><span class="mono">orders.ts:62</span> — 재고 차감을 주문 생성이 아니라 <b>결제 성공 후</b>로 이동 <span class="gray">(정책 ①)</span></li>
<li><span class="mono">admin.ts</span> — 실패 주문에 실패 사유 필드 노출 <span class="gray">(정책 ③)</span></li>
</ol>
<p class="gray">원하시면 payments.ts부터 수정 diff를 만들어 드릴게요.</p>'''),

  # 데모 ① 세션 B — 새 세션, "어제 정한 대로" → 모름 + 같은 질문 반복
  'mock-sessb': page('어제 정한 대로 결제 실패 처리 이어서 해줘', None, '''
<p><span class="hl">이전 대화 내용은 확인할 수 없습니다.</span> 현재 코드 기준으로 다시 정리했습니다.</p>
<p>진행하려면 다음을 먼저 결정해야 합니다.</p>
<ol>
<li>결제 실패 주문을 <b>보존</b>할까요, <b>삭제</b>할까요?</li>
<li>재고는 <b>주문 생성</b>과 <b>결제 성공</b> 중 언제 차감할까요?</li>
<li>관리자 화면에 실패 사유를 어디까지 노출할까요?</li>
</ol>
<p class="gray">참고 — 현재 <span class="mono">OrderStatus</span>는 pending | paid | cancelled 입니다.</p>'''),

  # 데모 ② 마지막 답변 — 결론만, 근거 없음 (C3 리캡용)
  'mock-demo2': page('결제 실패 상태 처리해줘', None, '''
<p><b>결제 실패 상태 처리를 구현했습니다.</b></p>
<p><span class="chip">M src/store.ts</span><span class="chip">M src/payments.ts</span><span class="chip">M src/admin.ts</span><span class="gray">&nbsp;+187줄</span></p>
<p><span class="mono">payment_failed</span> 상태를 추가하고, 결제 실패 시 주문을 보존하도록 수정했으며, 관리자 조회에 실패 주문이 포함되도록 변경했습니다.</p>
<p>이제 결제 실패가 정상적으로 처리됩니다.</p>'''),
}

os.makedirs('/home/claude/webapp/assets', exist_ok=True)
for name, html in MOCKS.items():
    src = f'/tmp/{name}.html'
    open(src, 'w', encoding='utf-8').write(html)
    subprocess.run(['/opt/pw-browsers/chromium', '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', '--virtual-time-budget=6000',
                    f'--screenshot=/home/claude/webapp/assets/{name}.png',
                    '--window-size=1440,505', f'file://{src}'],
                   capture_output=True)
    print(name, os.path.getsize(f'/home/claude/webapp/assets/{name}.png'))
