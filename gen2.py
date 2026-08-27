# -*- coding: utf-8 -*-
"""플랜 HTML의 .mk 목업을 풀사이즈 HTML 슬라이드로 변환 — 애니메이션 + 키보드 내비"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PLANS = [
    dict(id='lec00', num='0강', title='오리엔테이션',
         sub='강의 소개 · 전체 지도 · 준비물', dur='약 15~20분',
         src=os.path.join(ROOT, 'ref/lecture00-orientation-plan-v1.html'), cover='assets/cover00.png'),
    dict(id='lec01', num='1강', title='Codex를 써도 일이 안 줄어드는 4가지 패턴',
         sub='실패 재현 · 라이브 데모 3회 · 원인 진단', dur='약 45분',
         src=os.path.join(ROOT, 'ref/lecture01-slide-plan-v1.html'), cover='assets/cover01.png'),
    dict(id='lec02', num='2강', title='대화창 답변을 작업 자산으로 바꾸기',
         sub='사실/추정 분리 · 결정 질문 · 실습 4회', dur='약 45분',
         src=os.path.join(ROOT, 'ref/lecture02-slide-plan-v1.html'), cover='assets/cover02.png'),
    dict(id='lec03', num='3강', title='작업 경계 잡기: 어디까지 맡기고 어디서 멈출지',
         sub='요청 분해 · 금지 조건 · human gate · 멈춤 조건', dur='약 40분',
         src=os.path.join(ROOT, 'ref/lecture03-slide-plan-v1.html'), cover='assets/cover03.png'),
    dict(id='lec04', num='4강', title='Codex가 먼저 읽어야 할 기준 만들기',
         sub='AGENTS.md · 편집 전 기준 · 금지 규칙 · 도구 간 연결', dur='약 45분',
         src=os.path.join(ROOT, 'ref/lecture04-slide-plan-v1.html'), cover='assets/cover04.png'),
    dict(id='lec07', num='7강', title='도메인 정책 문서 만들기',
         sub='주문 상태 · 결제/재고 원칙 · 관리자 조회 · AGENTS.md 연결', dur='약 45분',
         src=os.path.join(ROOT, 'ref/lecture07-slide-plan-v1.html'), cover='assets/cover07.png'),
]
FONT = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">'

# ── 플랜에서 .mk CSS 블록 추출 (두 플랜 동일 — 0강 것 사용) ──
plan0 = open(PLANS[0]['src'], encoding='utf-8').read()
m = re.search(r'(\.mk\{.*?)\n\s*\.wf-spec', plan0, re.S)
MK_CSS = m.group(1)

# ── 섹션 파싱 ──
def parse(src):
    html = open(src, encoding='utf-8').read()
    out = []
    for sec in re.finditer(
            r'<span class="s-num">([^<]+)</span>.*?<h3>([^<]+)</h3>.*?<div class="mk">(.*?)</div>\s*<div class="cap">',
            html, re.S):
        out.append(dict(num=sec.group(1), title=sec.group(2), body=sec.group(3)))
    return out

VIEWER = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NUM__ __TITLE__ — 개발자를 위한 Codex</title>
__FONT__
<style>
  *{margin:0; padding:0; box-sizing:border-box;}
  html,body{height:100%;}
  body{font-family:Pretendard,-apple-system,sans-serif; background:#1c1c1e; overflow:hidden;
       -webkit-user-select:none; user-select:none;}
  #wrap{position:fixed; inset:0; display:flex; align-items:center; justify-content:center;}
  #stage{width:560px; height:315px; position:relative; box-shadow:0 18px 70px rgba(0,0,0,.45);}
  /* ── 슬라이드 (플랜 목업 CSS 그대로) ── */
  __MK_CSS__
  .mk{display:none; position:absolute; inset:0; width:560px; height:315px; aspect-ratio:auto; border:none;}
  .mk.on{display:block;}
  .mk.cover-img img{position:absolute; inset:0; width:100%; height:100%; object-fit:cover;}
  /* ── 진입 애니메이션 ── */
  @media (prefers-reduced-motion: no-preference){
    .mk.anim > *{opacity:0; transform:translateY(10px);
      transition:opacity .55s cubic-bezier(.2,.6,.2,1), transform .55s cubic-bezier(.2,.6,.2,1);}
    .mk.anim.go > *{opacity:1; transform:none;}
    .mk.anim > .lbl, .mk.anim > .mark{transition-delay:0ms !important;}
  }
  /* ── HUD ── */
  .hud{position:fixed; z-index:10; font-size:13px; color:rgba(255,255,255,.85);
       background:rgba(28,28,30,.62); backdrop-filter:blur(8px); border-radius:8px;
       padding:7px 12px; opacity:0; transition:opacity .25s;}
  body.hud-on .hud{opacity:1;}
  #ctr{right:16px; bottom:16px; cursor:pointer; font-variant-numeric:tabular-nums;}
  #ttl{left:16px; bottom:16px; max-width:52vw; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  #home{right:16px; top:16px; cursor:pointer; text-decoration:none;}
  .edge{position:fixed; top:0; bottom:0; width:30%; z-index:5; cursor:pointer;}
  /* ── 목차 오버레이 ── */
  #toc{position:fixed; inset:0; z-index:20; background:rgba(20,20,22,.97); overflow-y:auto;
       display:none; padding:56px 24px;}
  #toc.on{display:block;}
  #toc .list{max-width:640px; margin:0 auto;}
  #toc .row{display:flex; gap:14px; align-items:baseline; padding:11px 14px; border-radius:8px;
            cursor:pointer; color:#d8d8de; font-size:15px;}
  #toc .row:hover{background:rgba(255,255,255,.06);}
  #toc .row.cur{background:rgba(252,28,73,.14); color:#fff;}
  #toc .row .n{font-size:12px; font-weight:700; color:#FC1C49; min-width:34px; font-variant-numeric:tabular-nums;}
</style>
</head>
<body class="hud-on">
<div id="wrap"><div id="stage">
__SLIDES__
</div></div>
<div class="edge" style="left:0" onclick="go(-1)"></div>
<div class="edge" style="right:0" onclick="go(1)"></div>
<a class="hud" id="home" href="index.html">목차</a>
<div class="hud" id="ttl">__NUM__ · __TITLE__</div>
<div class="hud" id="ctr" onclick="toggleToc()" title="클릭: 슬라이드 목록">1 / __N__</div>
<div id="toc"><div class="list" id="tocList"></div></div>
<script>
var slides = Array.prototype.slice.call(document.querySelectorAll('#stage .mk'));
var TITLES = __TITLES__;
var N = slides.length, cur = -1, hudT = null;
var ctr = document.getElementById('ctr'), toc = document.getElementById('toc');

function fit(){
  var z = Math.min(innerWidth / 560, innerHeight / 315);
  var st = document.getElementById('stage');
  if ('zoom' in st.style) st.style.zoom = z;
  else { st.style.transform = 'scale(' + z + ')'; st.style.transformOrigin = 'center'; }
}
addEventListener('resize', fit); fit();

function show(i){
  i = Math.max(0, Math.min(N - 1, i));
  if (i === cur) return;
  if (cur >= 0) slides[cur].classList.remove('on', 'go');
  cur = i;
  var s = slides[cur];
  var kids = s.children;
  for (var k = 0; k < kids.length; k++)
    kids[k].style.transitionDelay = Math.min(80 + k * 65, 1150) + 'ms';
  s.classList.add('on');
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ s.classList.add('go'); }); });
  ctr.textContent = (cur + 1) + ' / ' + N;
  location.replace('#' + (cur + 1));
  wake();
}
function go(d){ if (toc.classList.contains('on')) return; show(cur + d); }
function wake(){
  document.body.classList.add('hud-on');
  clearTimeout(hudT);
  hudT = setTimeout(function(){ document.body.classList.remove('hud-on'); }, 2600);
}
var tocList = document.getElementById('tocList');
function toggleToc(){
  if (!tocList.childElementCount){
    TITLES.forEach(function(t, i){
      var r = document.createElement('div'); r.className = 'row';
      r.innerHTML = '<span class="n">' + t[0] + '</span><span>' + t[1] + '</span>';
      r.onclick = function(){ toggleToc(); show(i); };
      tocList.appendChild(r);
    });
  }
  toc.classList.toggle('on');
  if (toc.classList.contains('on')){
    var rows = tocList.children;
    for (var j = 0; j < rows.length; j++) rows[j].classList.toggle('cur', j === cur);
    if (rows[cur]) rows[cur].scrollIntoView({block: 'center'});
  }
}
document.addEventListener('keydown', function(e){
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); go(1); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(-1); }
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(N - 1);
  else if (e.key === 'f') { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
  else if (e.key === 'o' || e.key === 'g') toggleToc();
  else if (e.key === 'Escape') { if (toc.classList.contains('on')) toggleToc(); else location.href = 'index.html'; }
});
var tx = null;
document.addEventListener('touchstart', function(e){ tx = e.touches[0].clientX; }, {passive: true});
document.addEventListener('touchend', function(e){
  if (tx === null) return;
  var dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1);
  tx = null;
}, {passive: true});
document.addEventListener('mousemove', wake);
show(Math.max(0, (parseInt(location.hash.slice(1)) || 1) - 1));
</script>
</body>
</html>
'''

for L in PLANS:
    secs = parse(L['src'])
    L['n'] = len(secs)
    if L['cover']:
        parts = ['<section class="mk cover-img anim"><img src="%s" alt="표지"></section>' % L['cover']]
        titles = [['01', '표지']]
        rest = secs[1:]
    else:
        parts, titles, rest = [], [], secs
    for s in rest:
        parts.append('<section class="mk anim">%s</section>' % s['body'])
        titles.append([s['num'], s['title']])
    html = (VIEWER
            .replace('__MK_CSS__', MK_CSS)
            .replace('__SLIDES__', '\n'.join(parts))
            .replace('__TITLES__', json.dumps(titles, ensure_ascii=False))
            .replace('__NUM__', L['num']).replace('__TITLE__', L['title'])
            .replace('__N__', str(L['n'])).replace('__FONT__', FONT))
    open(os.path.join(ROOT, L['id'] + '.html'), 'w', encoding='utf-8').write(html)

# ── index.html ──
cards = ''
for L in PLANS:
    cards += f'''
    <a class="card" href="{L['id']}.html">
      <div class="thumb"><img src="{L.get('thumb') or L['cover'] or 'assets/cover02.png'}" alt="{L['num']} 표지" loading="lazy"></div>
      <div class="meta">
        <div class="num">{L['num']} · {L['dur']} · {L['n']}장</div>
        <div class="title">{L['title']}</div>
        <div class="sub">{L['sub']}</div>
      </div>
    </a>'''
index = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>개발자를 위한 Codex — 강의 자료</title>
{FONT}
<style>
  *{{margin:0; padding:0; box-sizing:border-box;}}
  body{{font-family:Pretendard,-apple-system,sans-serif; background:#F5F5F5; color:#282828; min-height:100vh;}}
  .wrap{{max-width:1080px; margin:0 auto; padding:64px 24px 80px;}}
  .kicker{{font-size:15px; font-weight:700; color:#FC1C49; letter-spacing:.02em;}}
  h1{{font-size:38px; font-weight:800; margin:10px 0 6px;}}
  .desc{{font-size:15px; color:#5B5B5B; margin-bottom:44px;}}
  .hr{{height:1px; background:#E6E6E6; margin:0 0 44px;}}
  .grid{{display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:28px;}}
  .card{{display:block; background:#fff; border-radius:12px; overflow:hidden; text-decoration:none; color:inherit;
        border:1px solid #E6E6E9; transition:transform .15s ease, box-shadow .15s ease;}}
  .card:hover{{transform:translateY(-3px); box-shadow:0 10px 30px rgba(40,40,40,.10);}}
  .thumb{{aspect-ratio:16/9; background:#EDEDF0; border-bottom:1px solid #EFEFEF;}}
  .thumb img{{width:100%; height:100%; object-fit:cover; display:block;}}
  .meta{{padding:18px 20px 22px;}}
  .num{{font-size:12.5px; font-weight:700; color:#9C9C9C; margin-bottom:6px;}}
  .title{{font-size:18px; font-weight:800; line-height:1.35; margin-bottom:6px;}}
  .sub{{font-size:13.5px; color:#5B5B5B;}}
  .foot{{margin-top:56px; font-size:12.5px; color:#B3B3B3;}}
  kbd{{background:#EDEDF0; border-radius:4px; padding:1px 6px; font-family:inherit; font-size:11.5px; color:#3C3C42;}}
</style>
</head>
<body>
<div class="wrap">
  <div class="kicker">개발자를 위한 Codex</div>
  <h1>강의 자료</h1>
  <div class="desc">2 Part · 4 Chapter · 20강 — 강의를 열고 <kbd>←</kbd> <kbd>→</kbd> 로 넘기세요 · <kbd>F</kbd> 전체화면 · <kbd>O</kbd> 슬라이드 목록</div>
  <div class="hr"></div>
  <div class="grid">{cards}
  </div>
  <div class="foot">Fast campus · 개발자를 위한 Codex</div>
</div>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(index)
print('generated:', ', '.join('%s (%d장)' % (L['id'], L['n']) for L in PLANS))
