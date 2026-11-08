#!/usr/bin/env python3
"""Build dashboard v5: CDC WONDER firearm mortality 1999-2020 by intent,
into the National tab. Run from ~/workspace/violence-intelligence/rebuild/."""
import json

SRC = '/home/hatch/workspace/violence-intelligence/rebuild/index.html'
with open(SRC) as f:
    html = f.read()

def sub(old, new):
    global html
    assert old in html, 'ANCHOR NOT FOUND: ' + old[:90]
    html = html.replace(old, new, 1)

with open('/home/hatch/workspace/violence-intelligence/rebuild/data/national-wonder.json') as f:
    w = json.load(f)

years = w['years']
max_t = max(y['total'] for y in years)
bars = ''
for y in years:
    wt = round(y['total'] / max_t * 100)
    ws = round(y['suicide'] / max_t * 100)
    wh = round(y['homicide'] / max_t * 100)
    bars += (f'<div class="bar-row"><span class="bar-label">{y["year"]}</span>'
             f'<div class="bar-track"><div class="bar" style="width:{wt}%"></div></div>'
             f'<span class="bar-value">{y["total"]:,}</span>'
             f'<span class="bar-sub">suicide {y["suicide"]:,} · homicide {y["homicide"]:,}</span></div>\n')

sub('<small>Public research · Chicago pilot · v4 — national data live</small>',
    '<small>Public research · Chicago pilot · v5 — national data live</small>')

anchor = '<div class="panel" style="margin-top:13px"><h2>National expansion: data-readiness before rankings</h2>'
wonder = f'''<div class="panel" style="margin-top:13px"><h2>All firearm deaths, by intent — United States, 1999–2020</h2>
<p class="method">Source: CDC WONDER, Underlying Cause of Death 1999–2020 (dataset D76), retrieved 2026-11-08. Death certificates, ICD-10 codes X72–X74 (suicide), X93–X95 (assault/homicide), W32–W34 (accidental), Y22–Y24 (undetermined intent). The 11-code query was run twice with identical results; W34 was queried separately. One cell flagged Unreliable in the source: Y23 in 2020 (19 deaths).</p>
<div class="bars">
{bars}</div>
<p class="method"><strong>The shape of the problem is not what most people assume.</strong> In 2020, of 44,610 firearm deaths, suicide was 24,292 (54.5%) and homicide 19,383 (43.4%); accidental 535 and undetermined 400 made up the rest. Suicide has been the majority of U.S. firearm deaths in every year of this series — 16,599 of 28,575 in 1999 (58.1%). Homicide is the more volatile series: flat near 11,000–12,000 through 2014, then 12,974 (2015) → 14,542 (2017) → 19,383 (2020, +33% in one year). Total firearm deaths rose from 28,575 (1999) to 44,610 (2020, +56%).</p>
<p class="method"><strong>Two systems, shown separately.</strong> WONDER counts deaths on death certificates; the FBI series above counts offenses reported by police. They do not cover the same universe — e.g. WONDER records 12,974 firearm homicides in 2015 against the FBI's 15,643 homicide offenses — so the two are never merged into one number. Both are shown because each answers a different question: how many people died, and how many offenses were reported.</p></div>
'''
sub(anchor, wonder + anchor)

with open(SRC, 'w') as f:
    f.write(html)
print('v5 transform OK,', len(html), 'bytes')
