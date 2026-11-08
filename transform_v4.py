#!/usr/bin/env python3
"""Build dashboard v4: national trends + SHR circumstance breakdown from the
FBI Crime Data Explorer (fetched live 2026-11-08), into the National tab.
Run from ~/workspace/violence-intelligence/rebuild/."""
import json

SRC = '/home/hatch/workspace/violence-intelligence/rebuild/index.html'
with open(SRC) as f:
    html = f.read()

def sub(old, new):
    global html
    assert old in html, 'ANCHOR NOT FOUND: ' + old[:90]
    html = html.replace(old, new, 1)

with open('/home/hatch/workspace/violence-intelligence/rebuild/data/national-cde.json') as f:
    nat = json.load(f)

annual = nat['annual_homicide']
max_h = max(a['homicides'] for a in annual)
bars = ''
for a in annual:
    w = round(a['homicides'] / max_h * 100)
    flag = ' <span class="warn">⚠ 2021 coverage 74–80% — understated, not a decline</span>' if a['year'] == 2021 else ''
    bars += (f'<div class="bar-row"><span class="bar-label">{a["year"]}</span>'
             f'<div class="bar-track"><div class="bar" style="width:{w}%"></div></div>'
             f'<span class="bar-value">{a["homicides"]:,}</span>{flag}</div>\n')

groups = nat['shr_national_2015_2024']['groups']
grows = ''
for g in groups:
    known = f'{g["share_of_known_pct"]:.1f}% of known' if g['share_of_known_pct'] is not None else '—'
    grows += (f'<tr><td><strong>{g["group"]}</strong></td><td>{g["count"]:,}</td>'
              f'<td>{g["share_of_all_pct"]:.1f}%</td><td>{known}</td>'
              f'<td>{g["note"]}</td></tr>\n')

sub('<small>Public research · Chicago pilot · v3</small>',
    '<small>Public research · Chicago pilot · v4 — national data live</small>')

old_nat = '''<section id="national" class="hidden"><div class="panel"><h2>National expansion: data-readiness before rankings</h2><p>The platform is designed to expand from Chicago to ten consistently selected U.S. cities. A defensible top-ten list is not yet populated: comparing agencies without matching population, offense definitions and reporting coverage would produce misleading rankings.</p><div class="national-steps"><div class="panel"><strong>01 · Define the population</strong><p>Cities above a predeclared population threshold; distinguish municipal city boundaries from police-agency service areas.</p></div><div class="panel"><strong>02 · Compare like with like</strong><p>Use one calendar year, FBI violent-crime offense definitions, valid annual population denominators and verified agency reporting coverage.</p></div><div class="panel"><strong>03 · Rank and verify</strong><p>Publish rates per 100,000, months reported, sources and missingness. The actual top ten will be computed only after data-quality checks.</p></div></div><div class="notice">Current verified national city rankings in this application: <strong>none</strong>. Chicago is the first local research environment, not an assertion that it ranks in the national top ten.</div><p class="method">For national data, use <a href="https://cde.ucr.cjis.gov/" target="_blank" rel="noopener">FBI Crime Data Explorer</a>. After validation, the same map interface can provide a city selector and consistent legends. City-level violence rates and neighborhood-level victimization counts should never be conflated.</p></div></section>'''

new_nat = f'''<section id="national" class="hidden">
<div class="panel"><h2>United States — homicide trend, 2015–2024</h2>
<p class="method">Source: FBI Crime Data Explorer API, summarized national homicide (offense HOM), retrieved 2026-11-08. Reported counts from participating agencies — <strong>not</strong> FBI estimates. Monthly actuals summed to annual totals.</p>
<div class="bars">
{bars}</div>
<p class="method">Homicides rose from 15,643 (2015) to 21,591 (2020, +38%), stayed high in 2022 (21,884), then fell to 17,277 in 2024. <strong>Read 2021 with care:</strong> only 74–80% of the U.S. population was covered that year as agencies switched to NIBRS reporting, so its 17,932 is understated — the dip is a coverage artifact, not a decline. All other years covered 95–98% of the population.</p></div>
<div class="panel" style="margin-top:13px"><h2>Why homicides happen — the national circumstance picture, 2015–2024</h2>
<p class="method">Source: FBI Crime Data Explorer, Expanded Homicide (SHR) national totals, 2015–2024. 165,675 homicide victims. Circumstance groups below are the project's own grouping of the FBI's 27 circumstance categories; the expressive/instrumental split is a <strong>research signal</strong>, never a label on any incident.</p>
<table><thead><tr><th>Circumstance group</th><th>Victims</th><th>Share of all</th><th>Share of known</th><th>What's inside</th></tr></thead><tbody>
{grows}</tbody></table>
<p class="method"><strong>The headline is the unknown.</strong> In 44.0% of U.S. homicides (72,816 of 165,675), the facts provided do not permit determination of circumstances. Of the 92,859 with a known circumstance, arguments dominate: expressive-leaning (arguments, domestic violence, brawls) is 46.1% of known circumstances, against 15.4% felony-type (instrumental-leaning) and 6.6% gang. That is the national version of the question this platform exists to answer — and the 44% unknown is why the circumstance database matters: every incident coded is one fewer unknown.</p></div>
<div class="panel" style="margin-top:13px"><h2>Weapons, nationally, 2015–2024</h2>
<p class="method">Same SHR totals, 165,675 victims. <strong>Firearms: 121,569 victims, 73.4%</strong> (handgun 71,343; firearm type not specified 41,681; rifle 4,086; shotgun 2,129; other firearm 2,330). Knife/cutting instrument 15,924 (9.6%); personal weapons (hands, fists, feet) 6,994 (4.2%); blunt object 4,060 (2.4%); all other weapons 17,128 (10.3%).</p></div>
<div class="panel" style="margin-top:13px"><h2>National expansion: data-readiness before rankings</h2>
<p>The platform is designed to expand from Chicago to ten consistently selected U.S. cities. A defensible top-ten list is not yet populated: comparing agencies without matching population, offense definitions and reporting coverage would produce misleading rankings.</p><div class="national-steps"><div class="panel"><strong>01 · Define the population</strong><p>Cities above a predeclared population threshold; distinguish municipal city boundaries from police-agency service areas.</p></div><div class="panel"><strong>02 · Compare like with like</strong><p>Use one calendar year, FBI violent-crime offense definitions, valid annual population denominators and verified agency reporting coverage.</p></div><div class="panel"><strong>03 · Rank and verify</strong><p>Publish rates per 100,000, months reported, sources and missingness. The actual top ten will be computed only after data-quality checks.</p></div></div><div class="notice">Current verified national city rankings in this application: <strong>none</strong>. Chicago is the first local research environment, not an assertion that it ranks in the national top ten. National totals above come from the FBI Crime Data Explorer; city-level rates still need the same coverage checks.</div><p class="method">National firearm-mortality trends (CDC WONDER) are next: the API is verified working and a multi-year query is in flight. State-level series need the CDC NVSS mortality files, since the WONDER API is national-only.</p></div>
</section>'''

sub(old_nat, new_nat)

with open(SRC, 'w') as f:
    f.write(html)
print('v4 transform OK,', len(html), 'bytes')
