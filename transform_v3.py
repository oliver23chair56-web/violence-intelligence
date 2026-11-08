#!/usr/bin/env python3
"""Build dashboard v3: add escalation pathways + circumstance database
sections to the Research tab, and bump the version marker.
Run from ~/workspace/violence-intelligence/rebuild/."""
SRC = '/home/hatch/workspace/violence-intelligence/rebuild/index.html'

with open(SRC) as f:
    html = f.read()

def sub(old, new):
    global html
    assert old in html, 'ANCHOR NOT FOUND: ' + old[:90]
    html = html.replace(old, new, 1)

sub('<small>Public research · Chicago pilot · v2</small>',
    '<small>Public research · Chicago pilot · v3</small>')

pathways = '''<div class="panel" style="margin-top:13px"><h2>How arguments escalate — a framework to test, not a finding</h2>
<p class="method">Most shootings are not a bolt from nowhere. The research question is what turns an ordinary conflict into violence — and where, exactly, it becomes hard to stop. This framework codes each incident as a sequence, so patterns can be counted instead of assumed. It is a hypothesis. The database exists to test it.</p>
<h3>The pathway (8 stages)</h3>
<p class="method"><strong>1 Encounter</strong> — who meets whom, where, with what history &nbsp;→&nbsp; <strong>2 Trigger</strong> — the event that starts it &nbsp;→&nbsp; <strong>3 Interpretation</strong> — what each side thinks it meant (where misunderstandings live) &nbsp;→&nbsp; <strong>4 Challenge / response</strong> — the exchange, usually about status even when the words are about something else &nbsp;→&nbsp; <strong>5 Escalation</strong> — each step narrows the exits &nbsp;→&nbsp; <strong>6 Point of no return</strong> — after this, only outside intervention stops it &nbsp;→&nbsp; <strong>7 Violence</strong> &nbsp;→&nbsp; <strong>8 Aftermath</strong> — flight, and retaliation risk, which is often the trigger of the <em>next</em> incident.</p>
<p class="method">Most incidents never pass stage 4. The database will show which combinations of trigger + misunderstanding + context do pass it, and how often.</p>
<h3>Six misunderstandings that turn conflict violent</h3>
<table><thead><tr><th>Misunderstanding</th><th>What was misread</th></tr></thead><tbody>
<tr><td><strong>Misread intent</strong></td><td>A neutral or ambiguous act is read as a threat. People primed by prior violence read hostility into noise.</td></tr>
<tr><td><strong>Misread words</strong></td><td>An insult was not intended — a joke, a test, talk — but landed as a challenge. Accounts of what was said disagree.</td></tr>
<tr><td><strong>Misread audience</strong></td><td>Others are watching. Backing down in front of peers costs status; the same words alone would have ended it.</td></tr>
<tr><td><strong>Misread capability</strong></td><td>A weapon's presence changes what each side thinks the other will do — "if I don't, he will" — and shortens the time to act.</td></tr>
<tr><td><strong>Misread relationship</strong></td><td>Strangers treated as rivals, or acquaintances treated as strangers.</td></tr>
<tr><td><strong>No face-saving exit</strong></td><td>Neither side could stop without losing face, and no third party offered one. A structural trap, not a misread fact.</td></tr>
</tbody></table>
<h3 style="margin-top:16px">Where it could have stopped</h3>
<p class="method">Every stage has an exit: a clarifying response at stage 3; a third party stepping in, or one side leaving, at stage 4; interruption at stage 5. Past stage 6, almost none — that is the honest finding this framework expects. Prevention is built from these points: an intervention that works at stage 3 is a different product from one that works at stage 5.</p>
<p class="hint">Grounded in: Luckenbill (1977, homicide as a situated transaction); Felson &amp; Tedeschi (violence as response to perceived rule-breaking); Collins (confrontational tension); Athens (violentization); Katz ("righteous slaughter"). Full framework: research/escalation-taxonomy-v1.md in the project repository.</p></div>
<div class="panel" style="margin-top:13px"><h2>The circumstance database — being built now</h2>
<p class="method">The core of this project: a database of the circumstances behind every incident. One row per incident per circumstance code, stored <strong>verbatim</strong> as the source reported it; motive and escalation coding live in separate tables as <strong>signals</strong>, never as facts about the incident. Unknown is stored as a value, never filled in by guessing. Nothing is published until a named human reviewer approves it.</p>
<table><thead><tr><th>Table</th><th>Holds</th><th>Status</th></tr></thead><tbody>
<tr><td><code>incident_circumstances</code></td><td>Verbatim circumstance codes per incident</td><td>Schema designed</td></tr>
<tr><td><code>motive_signals</code></td><td>Expressive / instrumental signal + confidence + basis codes</td><td>Schema designed</td></tr>
<tr><td><code>escalation_pathways</code></td><td>Stage reached, trigger, misunderstandings, mechanisms, exits, retaliation links</td><td>Schema designed</td></tr>
<tr><td><code>circumstance_sources</code></td><td>Registry of every source table, with coverage and retrieval date</td><td>Schema designed</td></tr>
</tbody></table>
<p class="method"><strong>Status today:</strong> schema designed (migration 0002 in the repository); 0 incidents coded; seed aggregates (Illinois 2018, FBI 2018) already live in the benchmarks. Next: apply the migration to the live database, ingest the Illinois state-submitted table (74,884 records) as the first incident-level source, and reconcile its denominators before publishing any share computed on them.</p></div>
'''
sub('<div class="panel" style="margin-top:13px"><h2>Methods &amp; coverage</h2>',
    pathways + '<div class="panel" style="margin-top:13px"><h2>Methods &amp; coverage</h2>')

with open(SRC, 'w') as f:
    f.write(html)

print('v3 transform OK,', len(html), 'bytes')
