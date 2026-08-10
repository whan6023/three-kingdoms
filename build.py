#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成三国融合页面 index.html（人物卡片含历史画像+电影角色图+演员照片+地图）"""
import json, os

REPO = "/tmp/three-kingdoms-repo"

def img_path(folder, name, ext=None):
    """返回图片相对路径，若文件不存在返回 None"""
    base = os.path.join(REPO, folder)
    if not os.path.isdir(base):
        return None
    for f in os.listdir(base):
        stem, e = os.path.splitext(f)
        if stem == name:
            return f"{folder}/{f}"
    return None

# 人物数据: (名字, 显示名+拼音, 备注, 电影配音演员, 电视剧演员, 历史画像名, 电影角色图名)
PEOPLE = [
    # ==== 核心（两个渠道都有） ====
    ("曹操","曹操<br><span class=py>Cáo Cāo</span>","字孟德","檀健次","于和伟","曹操","曹操"),
    ("荀彧","荀彧<br><span class=py>Xún Yù</span>","彧 yù","囧森瑟夫","王劲松","荀彧","荀彧"),
    ("夏侯惇","夏侯惇<br><span class=py>Xiàhóu Dūn</span>","惇 dūn","肖合来提·艾尼","杨涵斌","夏侯惇","夏侯惇"),
    ("曹洪","曹洪<br><span class=py>Cáo Hóng</span>","字子廉","巽辰","陈之辉","曹洪","曹洪"),
    ("张郃","张郃<br><span class=py>Zhāng Hé</span>","郃 hé","一舟","郭家诺","张郃","张郃"),
    ("汉献帝·刘协","汉献帝 · 刘协<br><span class=py>Liú Xié</span>","末代天子","旺旺","王茂蕾","汉献帝","刘协"),
    ("董承","董承<br><span class=py>Dǒng Chéng</span>","","杨卫","赵彦民","董承","董承"),
    ("许褚","许褚<br><span class=py>Xǔ Chǔ</span>","褚 chǔ","良生","李龙","许褚","许褚"),
    ("郭嘉","郭嘉<br><span class=py>Guō Jiā</span>","字奉孝","","曹磊","郭嘉",""),
    # ==== 仅电影 ====
    ("袁绍","袁绍<br><span class=py>Yuán Shào</span>","字本初","路金波","","袁绍","袁绍"),
    ("许攸","许攸<br><span class=py>Xǔ Yōu</span>","攸 yōu","任俊鹏","","许攸","许攸"),
    ("麦子","麦子<br><span class=py>Mài zi</span>","曹操的狗","方浩然","","","麦子"),
    ("渠穆","渠穆<br><span class=py>Qú Mù</span>","渠 qú","沉寂","","","渠穆"),
    ("师父","师父<br><span class=py>Shīfu</span>","易中天客串","易中天","","","师父"),
    ("童子","童子<br><span class=py>Tóngzǐ</span>","","李潇宇","","","童子"),
    # ==== 仅电视剧 ====
    ("司马懿","司马懿<br><span class=py>Sīmǎ Yì</span>","懿 yì","","吴秀波","司马懿",""),
    ("张春华","张春华<br><span class=py>Zhāng Chūnhuá</span>","","","刘涛","张春华",""),
    ("曹丕","曹丕<br><span class=py>Cáo Pī</span>","字子桓","","李晨","曹丕",""),
    ("柏灵筠","柏灵筠<br><span class=py>Bǎi Língyún</span>","柏 bǎi","","张钧甯","",""),
    ("郭照","郭照<br><span class=py>Guō Zhào</span>","","","唐艺昕","郭照",""),
    ("杨修","杨修<br><span class=py>Yáng Xiū</span>","字德祖","","翟天临","杨修",""),
    ("甄宓","甄宓<br><span class=py>Zhēn Fú</span>","宓 fú","","张芷溪","甄宓",""),
    ("曹植","曹植<br><span class=py>Cáo Zhí</span>","字子建","","王仁君","曹植",""),
    ("曹叡","曹叡<br><span class=py>Cáo Ruì</span>","叡 ruì","","刘欢","曹叡",""),
    ("诸葛亮","诸葛亮<br><span class=py>Zhūgě Liàng</span>","字孔明","","王洛勇","诸葛亮",""),
    ("曹真","曹真<br><span class=py>Cáo Zhēn</span>","字子丹","","章贺","曹真",""),
    ("曹休","曹休<br><span class=py>Cáo Xiū</span>","字文烈","","杜星奇","曹休",""),
    ("曹爽","曹爽<br><span class=py>Cáo Shuǎng</span>","字昭伯","","杜奕衡","曹爽",""),
    ("司马师","司马师<br><span class=py>Sīmǎ Shī</span>","字子元","","肖顺尧","司马师",""),
    ("司马昭","司马昭<br><span class=py>Sīmǎ Zhāo</span>","字子上","","檀健次","司马昭",""),
    ("司马孚","司马孚<br><span class=py>Sīmǎ Fú</span>","字叔达","","王东","司马孚",""),
    ("侯吉","侯吉<br><span class=py>Hóu Jí</span>","虚构角色","","来喜","",""),
]

# 生成卡片 HTML
cards = []
for name, disp, note, mv, tv, hist, mvchar in PEOPLE:
    hist_img = img_path("images/history", hist) if hist else None
    mv_img = img_path("images/actors", mv) if mv else None
    tv_img = img_path("images/actors", tv) if tv else None
    mvc_img = img_path("images/movie", mvchar) if mvchar else None
    note_html = f'<span class="note">{note}</span>' if note else ""

    # 左侧：历史画像（大图） + 电影角色图
    left_imgs = []
    if hist_img:
        left_imgs.append(f'<figure class="ph"><img src="{hist_img}" alt="{name}历史画像" loading="lazy"><figcaption>历史画像</figcaption></figure>')
    if mvc_img:
        left_imgs.append(f'<figure class="ph"><img src="{mvc_img}" alt="{name}电影形象" loading="lazy"><figcaption>电影《三国的星空》</figcaption></figure>')
    left_html = "".join(left_imgs) if left_imgs else '<div class="noimg">无画像</div>'

    # 右侧：电影配音演员 + 电视剧演员（横向两张）
    mv_html = (f'<figure class="ch"><img src="{mv_img}" alt="{mv}" loading="lazy">'
               f'<figcaption><span class="who">{mv}</span><span class="tag">电影配音</span></figcaption></figure>'
               if mv_img and mv else
               f'<figure class="ch empty"><div class="noimg">—</div>'
               f'<figcaption><span class="who dash">—</span><span class="tag">电影配音</span></figcaption></figure>')
    tv_html = (f'<figure class="ch"><img src="{tv_img}" alt="{tv}" loading="lazy">'
               f'<figcaption><span class="who">{tv}</span><span class="tag">电视剧演员</span></figcaption></figure>'
               if tv_img and tv else
               f'<figure class="ch empty"><div class="noimg">—</div>'
               f'<figcaption><span class="who dash">—</span><span class="tag">电视剧演员</span></figcaption></figure>')

    cards.append(f'''
    <div class="card">
      <div class="left">{left_html}</div>
      <div class="info">
        <div class="nm">{disp}</div>
        {note_html}
        <div class="channels">
          {mv_html}
          {tv_html}
        </div>
      </div>
    </div>''')

cards_html = "\n".join(cards)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>三国 · 人物与地图</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  background:#fff;color:#222;line-height:1.6;
}}
.wrap{{max-width:1120px;margin:0 auto;padding:32px 20px 56px;}}
h1{{font-size:26px;font-weight:700;letter-spacing:0.04em;}}
.lead{{font-size:13.5px;color:#555;margin:10px 0 4px;}}
.lead b{{color:#222;}}
h2{{
  font-size:16px;color:#a0482e;border-bottom:2px solid #eee;
  padding-bottom:5px;margin:28px 0 14px;letter-spacing:0.06em;
}}
.sub{{font-size:12.5px;color:#888;margin:-8px 0 12px;}}

/* 人物卡片 */
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(500px,1fr));gap:18px;}}
.card{{
  display:flex;gap:18px;background:#fafafa;border:1px solid #e8e8e8;
  border-radius:12px;padding:18px;align-items:flex-start;
}}
.left{{flex:0 0 auto;display:flex;flex-direction:column;gap:10px;}}
.ph{{margin:0;width:190px;}}
.ph img{{width:190px;height:230px;object-fit:cover;border-radius:8px;display:block;background:#eee;}}
.ph figcaption{{font-size:11px;color:#999;text-align:center;margin-top:4px;}}
.info{{flex:1;min-width:0;}}
.nm{{font-size:20px;font-weight:700;}}
.nm .py{{display:block;font-size:12px;font-weight:400;color:#a0482e;margin-top:2px;}}
.note{{display:block;font-size:12px;color:#888;margin-top:3px;}}
.channels{{display:flex;gap:14px;margin-top:14px;}}
.ch{{flex:1;margin:0;text-align:center;background:#fff;border:1px solid #eee;border-radius:10px;padding:12px 10px 10px;}}
.ch img{{width:96px;height:118px;object-fit:cover;border-radius:6px;display:block;margin:0 auto 8px;background:#eee;}}
.ch figcaption{{font-size:12.5px;}}
.ch .who{{display:block;font-weight:600;}}
.ch .who.dash{{color:#ccc;font-weight:400;}}
.ch .tag{{display:block;font-size:10.5px;color:#999;margin-top:2px;}}
.ch.empty .noimg{{width:96px;height:118px;border-radius:6px;background:#f5f5f5;display:flex;align-items:center;justify-content:center;color:#ccc;margin:0 auto 8px;}}
.noimg{{display:flex;align-items:center;justify-content:center;color:#bbb;font-size:12px;}}

/* 地图 */
.map-frame{{border:1px solid #e8e8e8;border-radius:8px;background:#fafafa;padding:10px;}}
.map-frame svg{{width:100%;height:auto;display:block;}}
.ml{{font-family:inherit;fill:#333;}}
.ml.s{{fill:#888;}}
.legend{{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:#666;margin:8px 0;}}
.legend .dot{{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px;vertical-align:-1px;}}
.legend .r{{background:#c9a227;}}
.legend .b{{background:#a8402e;}}
.legend .p{{background:#4f8f7c;border-radius:2px;}}
table.geo{{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:6px;}}
.geo th,.geo td{{padding:7px 9px;text-align:left;border-bottom:1px solid #eee;vertical-align:top;}}
.geo th{{font-size:11.5px;color:#a0482e;background:#fafafa;white-space:nowrap;}}
.geo td.a{{font-weight:600;white-space:nowrap;color:#8a3a24;}}
.geo td.m{{white-space:nowrap;}}
.geo tbody tr:nth-child(even){{background:#fafafa;}}
.footnote{{font-size:11.5px;color:#999;text-align:center;margin-top:28px;border-top:1px solid #eee;padding-top:14px;}}
@media (max-width:560px){{
  .cards{{grid-template-columns:1fr;}}
  .card{{flex-direction:column;}}
  .left{{flex-direction:row;}}
  .ph{{width:140px;}}
  .ph img{{width:140px;height:170px;}}
}}
</style>
</head>
<body>
<div class="wrap">
  <h1>三国 · 人物与地图</h1>
  <p class="lead">
    融合两部作品：<b>动画电影《三国的星空第一部》</b>（讨董→官渡，曹操视角）与
    <b>电视剧《大军师司马懿》</b>（军师联盟 / 虎啸龙吟）。
    每个角色标注历史画像、电影角色形象、电影配音演员与电视剧演员；单渠道出现的人物另一栏留空。
  </p>

  <h2>人物</h2>
  <p class="sub">左侧为历史画像与电影角色形象，右侧为电影/电视剧两渠道扮演者照片。照片为演员本人公开照。</p>
  <div class="cards">
{cards_html}
  </div>

  <h2>地点舆图</h2>
  <p class="sub">方位示意，非精确测绘。黄线＝行军/北伐路线，红点＝战役地点，绿块＝势力中心。</p>
  <div class="legend">
    <span><span class="dot r"></span>行军/北伐路线</span>
    <span><span class="dot b"></span>战役地点</span>
    <span><span class="dot p"></span>势力中心</span>
  </div>
  <div class="map-frame">
    <svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
      <path d="M 90 240 C 180 215, 260 250, 380 230 C 450 215, 520 230, 640 205" fill="none" stroke="#6b8fae" stroke-width="2.5" opacity="0.35"></path>
      <text x="100" y="232" class="ml s" font-size="12">黄河</text>
      <path d="M 200 420 C 300 395, 400 430, 520 405 C 600 390, 660 400, 740 385" fill="none" stroke="#6b8fae" stroke-width="2.5" opacity="0.35"></path>
      <text x="210" y="440" class="ml s" font-size="12">长江</text>
      <path d="M 150 250 C 200 300, 240 330, 290 350" fill="none" stroke="#6b8fae" stroke-width="2" opacity="0.3" stroke-dasharray="4 4"></path>
      <text x="210" y="320" class="ml s" font-size="11">秦岭</text>
      <g transform="translate(748,44)" opacity="0.6">
        <line x1="0" y1="14" x2="0" y2="-14" stroke="#c9a227" stroke-width="1.4"></line>
        <path d="M0 -14 L -5 -4 L 5 -4 Z" fill="#c9a227"></path>
        <text x="0" y="-20" text-anchor="middle" class="ml" font-size="12" font-weight="700">北</text>
      </g>
      <path d="M312 372 L262 282 L245 244 L152 258" fill="none" stroke="#c9a227" stroke-width="2" stroke-dasharray="7 6" opacity="0.85"></path>
      <path d="M169.5 228.9 L346.8 207.6 L417.7 242.9" fill="none" stroke="#c9a227" stroke-width="1.6" stroke-dasharray="5 5" opacity="0.5"></path>
      <rect x="336.8" y="197.6" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="342.8" y="188" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">洛阳</text>
      <text x="342.8" y="230" text-anchor="middle" class="ml s" font-size="11">今洛阳市</text>
      <rect x="407.7" y="232.9" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="413.7" y="223" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">许都</text>
      <text x="413.7" y="265" text-anchor="middle" class="ml s" font-size="11">今许昌</text>
      <rect x="446.6" y="97.5" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="452.6" y="88" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">邺城</text>
      <text x="452.6" y="130" text-anchor="middle" class="ml s" font-size="11">今临漳</text>
      <rect x="159.5" y="218.9" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="165.5" y="209" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">长安</text>
      <text x="165.5" y="251" text-anchor="middle" class="ml s" font-size="11">今西安</text>
      <rect x="302" y="362" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="308" y="352" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">汉中</text>
      <text x="308" y="394" text-anchor="middle" class="ml s" font-size="11">蜀汉北伐基地</text>
      <rect x="662.5" y="336.6" width="12" height="12" fill="#4f8f7c"></rect>
      <text x="668.5" y="326" text-anchor="middle" class="ml" font-size="13.5" font-weight="700">江东</text>
      <text x="668.5" y="368" text-anchor="middle" class="ml s" font-size="11">今南京一带</text>
      <circle cx="423.7" cy="203.7" r="6.5" fill="#a8402e"></circle>
      <text x="423.7" y="128" text-anchor="middle" class="ml" font-size="13" font-weight="700">官渡</text>
      <text x="423.7" y="146" text-anchor="middle" class="ml s" font-size="11">今中牟东北</text>
      <line x1="423.7" y1="150" x2="423.7" y2="197" stroke="#a8402e" stroke-width="1" opacity="0.5"></line>
      <circle cx="435.5" cy="171.2" r="6.5" fill="#a8402e"></circle>
      <text x="478" y="168" class="ml" font-size="13" font-weight="700">乌巢</text>
      <text x="478" y="186" class="ml s" font-size="11">今延津东南</text>
      <circle cx="393.8" cy="200.3" r="6.5" fill="#a8402e"></circle>
      <text x="393.8" y="182" text-anchor="middle" class="ml" font-size="13" font-weight="700">虎牢关</text>
      <circle cx="262" cy="282" r="6.5" fill="#a8402e"></circle>
      <text x="262" y="264" text-anchor="middle" class="ml" font-size="13" font-weight="700">祁山</text>
      <text x="262" y="306" text-anchor="middle" class="ml s" font-size="11">今甘肃礼县</text>
      <circle cx="245" cy="244" r="6.5" fill="#a8402e"></circle>
      <text x="245" y="226" text-anchor="middle" class="ml" font-size="13" font-weight="700">街亭</text>
      <text x="245" y="268" text-anchor="middle" class="ml s" font-size="11">马谡失守</text>
      <circle cx="152" cy="258" r="6.5" fill="#a8402e"></circle>
      <text x="120" y="278" text-anchor="middle" class="ml" font-size="13" font-weight="700">五丈原</text>
      <text x="120" y="296" text-anchor="middle" class="ml s" font-size="11">诸葛亮病逝</text>
      <circle cx="178" cy="228" r="6.5" fill="#a8402e"></circle>
      <text x="200" y="222" class="ml" font-size="13" font-weight="700">陈仓</text>
      <text x="200" y="240" class="ml s" font-size="11">郝昭守城</text>
      <circle cx="415.2" cy="483.7" r="6.5" fill="#a8402e"></circle>
      <text x="415.2" y="505" text-anchor="middle" class="ml" font-size="13" font-weight="700">赤壁</text>
      <text x="415.2" y="523" text-anchor="middle" class="ml s" font-size="11">今赤壁市</text>
      <circle cx="313.4" cy="422.1" r="6.5" fill="#a8402e"></circle>
      <text x="313.4" y="443" text-anchor="middle" class="ml" font-size="13" font-weight="700">长坂坡</text>
      <text x="313.4" y="461" text-anchor="middle" class="ml s" font-size="11">今当阳</text>
    </svg>
  </div>

  <h2>古今地点对照</h2>
  <table class="geo">
    <thead><tr><th>古地名</th><th>今地名</th><th>相关</th></tr></thead>
    <tbody>
      <tr><td class="a">许都（Xǔ Dū）</td><td class="m">河南许昌</td><td>曹操迎汉献帝定都，"挟天子以令诸侯"</td></tr>
      <tr><td class="a">洛阳（Luò Yáng）</td><td class="m">河南洛阳</td><td>东汉旧都；曹丕称帝后的魏都</td></tr>
      <tr><td class="a">邺城（Yè Chéng）</td><td class="m">河北临漳西南</td><td>曹操霸府，铜雀台所在</td></tr>
      <tr><td class="a">长安（Cháng'ān）</td><td class="m">陕西西安</td><td>董卓西迁；关中重镇</td></tr>
      <tr><td class="a">官渡（Guān Dù）</td><td class="m">河南中牟东北</td><td>官渡之战，曹操以少胜多</td></tr>
      <tr><td class="a">乌巢（Wū Cháo）</td><td class="m">河南延津东南</td><td>夜袭火烧袁绍粮仓</td></tr>
      <tr><td class="a">赤壁（Chì Bì）</td><td class="m">湖北赤壁</td><td>孙刘联军火攻大败曹操</td></tr>
      <tr><td class="a">汉中（Hàn Zhōng）</td><td class="m">陕西汉中</td><td>蜀汉北伐大本营</td></tr>
      <tr><td class="a">祁山（Qí Shān）</td><td class="m">甘肃礼县一带</td><td>诸葛亮六出祁山北伐</td></tr>
      <tr><td class="a">街亭（Jiē Tíng）</td><td class="m">甘肃秦安东北</td><td>马谡失守，北伐失利</td></tr>
      <tr><td class="a">五丈原（Wǔzhàng Yuán）</td><td class="m">陕西岐山南</td><td>诸葛亮病逝</td></tr>
      <tr><td class="a">陈仓（Chén Cāng）</td><td class="m">陕西宝鸡</td><td>郝昭坚守不下</td></tr>
    </tbody>
  </table>

  <p class="footnote">
    历史画像来源：维基百科/维基共享资源（多为明清刻本画像）· 电影角色形象与剧照来源：电影官方物料/媒体报道 · 演员照片为演员本人公开照 · 地点为方位示意 · 生僻字已注音 · 人物资料据豆瓣/百度百科
  </p>
</div>
</body>
</html>'''

with open(os.path.join(REPO, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("index.html generated, size:", len(html))

# 输出缺失图片提示
missing = []
for name, disp, note, mv, tv, hist, mvchar in PEOPLE:
    for who, folder, label in [(mv, "images/actors", "演员"), (tv, "images/actors", "演员"), (hist, "images/history", "画像"), (mvchar, "images/movie", "电影角色")]:
        if who and not img_path(folder, who):
            missing.append(f"{label}缺失: {who} ({name})")
if missing:
    print("缺失图片:")
    for m in missing:
        print("  ", m)
else:
    print("所有图片已就位")
