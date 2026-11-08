#!/usr/bin/env python3
"""Rebuild Violence Intelligence dashboard v2 from the live deployed index.html.

Adds: Research tab (expressive/instrumental methods + Illinois circumstance
family breakdown + FBI SHR + state-table reconciliation with flagged
inconsistencies), weekday + top-area charts on Overview, and a live
coverage/methods line. All numbers below were verified against the live
Supabase endpoints on 2026-11-08 (see ../TAKEOVER-NOTES.md and
live-site/ep-*.json). Nothing is invented: where the source conversation
disagrees with itself, the disagreement is shown, not silently resolved.
"""
import re, sys

SRC = '/home/hatch/workspace/violence-intelligence/rebuild/index.html'

with open(SRC) as f:
    html = f.read()

def sub(old, new, count=1):
    global html
    assert old in html, 'ANCHOR NOT FOUND: ' + old[:90]
    html = html.replace(old, new, count)

# --- 1. Title / header: mark v2 ---
sub('<title>Violence Intelligence | Research Observatory</title>',
    '<title>Violence Intelligence | Research Observatory</title>')
sub('<small>Public research · Chicago pilot</small>',
    '<small>Public research · Chicago pilot · v2</small>')

# --- 2. New Research tab button ---
sub('<button data-tab="national">National expansion</button>',
    '<button data-tab="national">National expansion</button><button data-tab="research">Research &amp; methods</button>')

# --- 3. Tab switching: include research section; hide common toolbar + stats on it ---
sub("['overview','mapview','circumstances','cases','national'].forEach(x=>$(x).classList.toggle('hidden',x!==b.dataset.tab))",
    "['overview','mapview','circumstances','cases','national','research'].forEach(x=>$(x).classList.toggle('hidden',x!==b.dataset.tab))")
html = html.replace("$('common').classList.toggle('hidden',['circumstances','cases','national'].includes(b.dataset.tab));$('stats').classList.toggle('hidden',['circumstances','cases','national'].includes(b.dataset.tab));",
                  "$('common').classList.toggle('hidden',['circumstances','cases','national','research'].includes(b.dataset.tab));$('stats').classList.toggle('hidden',['circumstances','cases','national','research'].includes(b.dataset.tab));")

# --- 4. Coverage line under the toolbar ---
sub('<span id="loadStatus" class="hint">Loading verified aggregates…</span>',
    '<span id="loadStatus" class="hint">Loading verified aggregates…</span><span id="coverageLine" class="hint"></span>')

# --- 5. Overview: weekday + top-areas panels (second grid row, before the 2021 notice) ---
sub('<div class="notice">2021 is not loaded because Chicago\'s public data endpoint returned repeated errors for that period. Other years are historical snapshots, not a live safety forecast. Distinct cases are not equivalent to victim counts.</div>',
    '''<div class="grid" style="margin-top:13px"><div class="panel"><h2>Day of week</h2><p>All imported years. Victimizations concentrate on weekend days; describes timing, not motive.</p><div id="weekdays" class="chart"></div><p class="hint">Day numbering as reported by the source feed (0 = Sunday).</p></div><div class="panel"><h2>Where victimizations concentrate</h2><p>Top community areas across all imported years, by gunshot victimizations. Raw counts, not per-capita rates.</p><div id="topAreas"></div></div></div><div class="notice">2021 is not loaded because Chicago's public data endpoint returned repeated errors for that period. Other years are historical snapshots, not a live safety forecast. Distinct cases are not equivalent to victim counts.</div>''')

# --- 6. Research section before the footer ---
research = '''<section id="research" class="hidden">
<div class="panel"><h2>Expressive vs. instrumental: a research signal, not a label</h2>
<p class="method">The platform's core research question is whether circumstance patterns can inform prevention. <strong>Expressive</strong> violence is driven by interpersonal conflict, revenge, or anger. <strong>Instrumental</strong> violence is planned to obtain something else: money, status, or power. No case on this dashboard has been assigned one of these labels. Circumstance codes are a <strong>research signal</strong> — a reason to look closer — never a determination of motive. The boundary between the two is fluid, and people move between categories over time.</p>
<p class="method">Mapping rule used here (signal only): argument / conflict / retaliation codes point toward expressive; robbery / felony-for-gain codes point toward instrumental; gang-associated codes are <strong>not</strong> automatically either. Every mapping below preserves the original code label and the share that is unknown.</p></div>
<div class="grid" style="margin-top:13px"><div class="panel"><h2>Illinois homicide circumstances · 2018, by family</h2>
<p>Official statewide source counts (874 records). Grouped here only to show the shape of the data; the grouping does not assign motives.</p>
<table><thead><tr><th>Family</th><th>Codes in family</th><th>Records</th><th>Share of 874</th></tr></thead><tbody>
<tr><td>Unknown — unable to determine</td><td>Unable to Determine</td><td>290</td><td>33.2%</td></tr>
<tr><td>Interpersonal</td><td>Other Arguments 187 · Argument Over Money or Property 15 · Lover's Triangle 13 · Fight Due to Influence of Alcohol 5 · Fight Due to Influence of Narcotics 2</td><td>222</td><td>25.4%</td></tr>
<tr><td>Gang-associated</td><td>Gang Killings 159 · Juvenile Gang Killings 17</td><td>176</td><td>20.1%</td></tr>
<tr><td>Felony-type</td><td>Narcotic Drug Law Violations 50 · Robbery 48 · Other Felony 12 · Suspected Felony Type 4 · Prostitution and Commercialized Vice 3 · Arson 3 · Larceny—Theft 2 · Gambling 2 · Other Sex Offense 1</td><td>125</td><td>14.3%</td></tr>
<tr><td>Other</td><td>Other 58 · Child Killed by Babysitter 3</td><td>61</td><td>7.0%</td></tr>
</tbody></table>
<p class="hint">Source: Illinois 2018 Supplemental Homicide Reporting, via the live circumstance-benchmarks endpoint (verified 2026-11-08). Statewide counts are not firearm-specific and are a different population from Chicago's 2020–2025 victim totals — do not compare them directly.</p></div>
<div class="panel"><h2>FBI Supplemental Homicide Report · 2018</h2>
<p>National context, same year, different reporting system:</p>
<div class="research-metrics"><div class="stat"><small>Known circumstances</small><div class="metrics-big">61%</div><small>Share with reported details</small></div><div class="stat"><small>Argument, among known</small><div class="metrics-big">39.4%</div><small>Not a share of all murders</small></div><div class="stat"><small>Felony-type, among known</small><div class="metrics-big">24.5%</div><small>Among known-circumstance murders</small></div></div>
<p class="method" style="margin-top:14px">These are percentages <strong>among murders with known circumstances</strong>, not of all murders, and not a direct measure of expressive violence. Source: FBI Crime Data Explorer, via the live circumstance-benchmarks endpoint.</p></div></div>
<div class="panel" style="margin-top:13px"><h2>Illinois 2018 homicide circumstances — verified against the source document</h2>
<p class="method">Illinois State Police, <em>Crime in Illinois 2018</em>, Section V — Supplemental Homicide Reporting. Statewide, 2018: <strong>845 homicide incidents, 894 victims</strong> (874 first/second-degree murder + 11 justifiable homicide + 9 involuntary manslaughter). The circumstance table below covers the 874 murder victims. These are <strong>not</strong> Chicago shooting data and not firearm-specific — a historical benchmark, not a comparison set.</p>
<table><thead><tr><th>Circumstance group</th><th>Victims</th><th>Share of 874</th><th>What\'s inside</th></tr></thead><tbody>
<tr><td>Unable to determine</td><td>290</td><td>33.2%</td><td>Unable to Determine</td></tr>
<tr><td>Interpersonal / argument</td><td>222</td><td>25.4%</td><td>Other Arguments 187, Argument Over Money/Property 15, Lover\'s Triangle 13, Fight — Alcohol 5, Fight — Narcotics 2</td></tr>
<tr><td>Gang</td><td>176</td><td>20.1%</td><td>Gang Killings 159, Juvenile Gang Killings 17</td></tr>
<tr><td>Felony-type</td><td>125</td><td>14.3%</td><td>Robbery 48, Narcotic Drug Law Violations 50, Other Felony 12, Suspected Felony 4, Arson 3, Prostitution 3, Larceny–Theft 2, Gambling 2, Other Sex Offense 1</td></tr>
<tr><td>Other</td><td>61</td><td>7.0%</td><td>Other 58, Child Killed by Babysitter 3</td></tr>
</tbody></table>
<div class="notice"><strong>Correction, 2026-11-08.</strong> An earlier version of this panel cited a 74,884-record "state-submitted" Illinois table. That table does not exist in any verified source and has been removed. The figures above are read directly from the ISP PDF and match the database and the live benchmarks endpoint (874).</div>
<p class="method">Ludwig / Maxwell Street Express framing is used here as a research lens — asking whether circumstance patterns cluster in ways prevention could act on — not as a classification rule. Literature named in the project: Cornell work on circumstantial categories mapping to groups of crimes; University of Chicago Crime Lab; Princeton gun-violence research; Sampson &amp; Laub (1993), <em>Law &amp; Society Review</em> 27(2), 285–311.</p></div>
<div class="panel" style="margin-top:13px"><h2>Methods &amp; coverage</h2>
<p class="method" id="methodsCoverage">Dataset: Chicago Violence Reduction — Victims. Grain: one row per gunshot victimization. Coverage: 2020 and 2022–2025 historical snapshots; 2021 was not imported. No motive classifications have been reviewed or published (0 reviewed motives). 2025 is the most recent snapshot and may be revised by the source. Counts are reported victimizations, not confirmed shootings, distinct victims, or adjudicated incidents. No incident-level maps, no personal identifiers, no predictive policing, no person-level risk scores. Raw circumstance tables are not published; only aggregated, anonymized breakdowns appear here.</p>
<p class="method">What would make this stronger next: import 2021; reconcile the state-table denominators against the Illinois State Police and FBI sources; add reviewed case narratives with human approval before any motive label is published; extend the same grain and definitions to additional cities before any ranking.</p></div>
</section>
'''
sub('<div class="source" id="footer">', research + '<div class="source" id="footer">')

# --- 7. JS: weekday + top-area charts in renderOverview ---
sub("showBars('locations',analytics.locations)}",
    """showBars('locations',analytics.locations);
const dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const wd=(analytics.weekdays||[]).slice().sort((a,b)=>a.day_of_week-b.day_of_week);
if(wd.length){const max=Math.max(1,...wd.map(x=>x.victimizations));$('weekdays').innerHTML='<div style="display:flex;gap:8px;align-items:end;height:190px">'+wd.map(x=>'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px"><div title="'+fmt(x.victimizations)+' victimizations" style="width:100%;height:'+Math.max(3,100*x.victimizations/max)+'%;background:linear-gradient(#52c7be,#276b85);border-radius:5px 5px 0 0"></div><span style="font-size:11px;color:#879baa">'+dayNames[x.day_of_week]+'</span><span style="font-size:11px;color:#c6d6df">'+fmt(x.victimizations)+'</span></div>').join('')+'</div>'}
showBars('topAreas',(analytics.areas||[]),'name','victimizations',10)}""")

# --- 8. JS: coverage line on successful analytics load ---
sub("$('loadStatus').textContent=x.annual.length+' imported years; 2021 missing';renderOverview()",
    """$('loadStatus').textContent=x.annual.length+' imported years; 2021 missing';
$('coverageLine').textContent='Dataset: '+(x.dataset||'Chicago Violence Reduction — Victims')+' · Grain: '+(x.grain||'victimization')+' · Generated '+(x.generated_at||'').slice(0,10)+' · Motives reviewed: none';
$('methodsCoverage').textContent+=' Data as generated '+(x.generated_at||'').slice(0,10)+'.';
renderOverview()""")

with open(SRC, 'w') as f:
    f.write(html)

print('transformed OK,', len(html), 'bytes')
