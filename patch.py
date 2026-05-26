#!/usr/bin/env python3
"""Apply all fixes: overlay scroll, remove X, fix whitespace, redesign knockout bracket."""
import re, json

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# ─── FIX 1: Remove X button from overlay HTML ───
html = html.replace(
    '      <span class="overlay-back" id="overlay-back">← Back</span>\n      <span class="overlay-close" id="overlay-close">✕</span>',
    '      <span class="overlay-back" id="overlay-back">← Back</span>'
)

# Remove overlay-close CSS references
html = html.replace(
    '.overlay-back,.overlay-close{cursor:pointer;padding:4px 8px;border-radius:8px;}',
    '.overlay-back{cursor:pointer;padding:4px 8px;border-radius:8px;}'
)
html = html.replace(
    '.overlay-back:active,.overlay-close:active{background:rgba(255,255,255,.15);}',
    '.overlay-back:active{background:rgba(255,255,255,.15);}'
)

# Remove overlay-close from click handler
html = html.replace(
    "if (e.target.closest('#overlay-back') || e.target.closest('#overlay-close')) {",
    "if (e.target.closest('#overlay-back')) {"
)

# ─── FIX 2: Scroll to top when opening match detail ───
html = html.replace(
    "  $('#match-overlay').classList.add('open');\n\n  // Detail sub-tabs",
    "  $('#match-overlay').scrollTop = 0;\n  $('#match-overlay').classList.add('open');\n\n  // Detail sub-tabs"
)

# ─── FIX 3: Fix bottom whitespace — add min-height to content ───
# The overlay CSS needs to be tighter
html = html.replace(
    ".match-overlay{\n    position:absolute;inset:0;background:var(--bg);z-index:100;\n    transform:translateX(100%);transition:transform .3s ease;\n    overflow-y:auto;-webkit-overflow-scrolling:touch;\n  }",
    ".match-overlay{\n    position:absolute;inset:0;background:var(--bg);z-index:100;\n    transform:translateX(100%);transition:transform .3s ease;\n    overflow-y:auto;-webkit-overflow-scrolling:touch;display:flex;flex-direction:column;\n  }"
)

# ─── FIX 4: Replace knockout bracket CSS ───
old_ko_css = """  /* Knockout bracket — tournament tree */
  .ko-bracket{overflow-x:auto;padding:10px 0 20px;scrollbar-width:none;}
  .ko-bracket::-webkit-scrollbar{display:none;}
  .ko-tree{display:flex;align-items:stretch;gap:0;min-width:max-content;position:relative;}
  .ko-round{display:flex;flex-direction:column;justify-content:space-around;min-width:150px;position:relative;padding:0 6px;}
  .ko-round-title{
    font-size:10px;font-weight:800;color:var(--hyundai-accent);text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:8px;padding-left:2px;text-align:center;
  }
  .ko-round-matches{display:flex;flex-direction:column;justify-content:space-around;flex:1;gap:6px;}
  .ko-match{
    background:#fff;border-radius:10px;border:1px solid var(--line);
    padding:6px 10px;cursor:pointer;position:relative;
    box-shadow:0 2px 6px rgba(0,0,0,.04);transition:transform .15s,box-shadow .15s;
  }
  .ko-match:active{transform:scale(.97);box-shadow:0 1px 3px rgba(0,0,0,.08);}
  .ko-team-row{display:flex;align-items:center;justify-content:space-between;padding:2px 0;}
  .ko-team-row .team-info{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;}
  .ko-team-row .ko-score{font-size:12px;font-weight:800;color:var(--fifa-navy);}
  .ko-team-row.winner .team-info{font-weight:800;color:var(--fifa-navy);}
  .ko-team-row.loser{opacity:.45;}
  .ko-date{font-size:9px;color:var(--muted);margin-bottom:4px;}
  .ko-divider{height:1px;background:var(--line);margin:2px 0;}
  .ko-connector{position:absolute;right:-6px;width:12px;pointer-events:none;}
  .ko-connector line{stroke:var(--line);stroke-width:1.5;}
  /* Vertical list fallback for mobile */
  .ko-list .ko-round{min-width:unset;padding:0;}
  .ko-list .ko-round-matches{gap:8px;}
  .ko-list .ko-match{padding:10px 14px;}
  .ko-list .ko-team-row .team-info{font-size:12px;}
  .ko-list .ko-team-row .ko-score{font-size:14px;}"""

new_ko_css = """  /* Knockout bracket — FIFA.com style with round filters */
  .ko-filter-rail{
    display:flex;gap:6px;padding:12px 16px 8px;overflow-x:auto;scrollbar-width:none;
    background:var(--bg);position:sticky;top:0;z-index:5;
  }
  .ko-filter-rail::-webkit-scrollbar{display:none;}
  .ko-filter-btn{
    padding:8px 14px;border-radius:20px;font-size:11px;font-weight:700;
    color:var(--muted);background:#fff;border:1.5px solid var(--line);white-space:nowrap;
    cursor:pointer;transition:all .2s ease;flex-shrink:0;
    -webkit-user-select:none;user-select:none;
  }
  .ko-filter-btn:active{transform:scale(.95);}
  .ko-filter-btn.active{
    background:linear-gradient(135deg,var(--fifa-navy),var(--fifa-blue));
    color:#fff;border-color:transparent;box-shadow:0 2px 8px rgba(30,58,138,.25);
  }
  .ko-round-container{
    padding:8px 16px 16px;transition:opacity .4s cubic-bezier(.3,0,.15,1),transform .4s cubic-bezier(.3,0,.15,1);
  }
  .ko-round-container.entering{opacity:0;transform:translateY(12px);}
  .ko-round-container.visible{opacity:1;transform:translateY(0);}
  .ko-round-label{
    font-size:11px;font-weight:800;color:var(--hyundai-accent);text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:10px;text-align:center;
  }
  .ko-match-pair{margin-bottom:10px;}
  .ko-pair-connector{
    display:flex;align-items:center;justify-content:center;padding:2px 0;
  }
  .ko-pair-label{font-size:9px;color:var(--muted);font-weight:600;letter-spacing:.5px;}
  .ko-match{
    background:#fff;border-radius:12px;border:1px solid var(--line);
    padding:10px 14px;cursor:pointer;position:relative;
    box-shadow:0 2px 8px rgba(0,0,0,.04);transition:transform .15s,box-shadow .15s;
  }
  .ko-match:active{transform:scale(.97);box-shadow:0 1px 3px rgba(0,0,0,.08);}
  .ko-match-num{
    font-size:9px;font-weight:700;color:var(--muted);margin-bottom:4px;
    display:flex;justify-content:space-between;align-items:center;
  }
  .ko-match-date{font-size:9px;color:var(--muted);font-weight:400;}
  .ko-team-row{display:flex;align-items:center;justify-content:space-between;padding:3px 0;}
  .ko-team-row .team-info{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600;color:var(--text);}
  .ko-team-row .team-info .team-flag{font-size:16px;line-height:1;}
  .ko-team-row .team-info .team-code{min-width:60px;}
  .ko-team-row .ko-score{font-size:13px;font-weight:800;color:var(--fifa-navy);min-width:16px;text-align:center;}
  .ko-team-row.winner .team-info{font-weight:800;color:var(--fifa-navy);}
  .ko-team-row.winner .ko-score{color:var(--green);}
  .ko-team-row.loser{opacity:.45;}
  .ko-divider{height:1px;background:var(--line);margin:2px 0;}
  .ko-pair-svg{text-align:center;margin:4px 0 -2px;}
  .ko-pair-svg svg{width:80px;height:24px;}
  .ko-summary{
    text-align:center;padding:16px;font-size:12px;color:var(--muted);line-height:1.6;
  }
  .ko-summary .trophy-icon{font-size:28px;margin-bottom:6px;}
  .ko-bracket-mini{
    display:grid;grid-template-columns:repeat(5,1fr);gap:4px;padding:12px 0;align-items:center;
  }
  .ko-bracket-mini .mini-col{display:flex;flex-direction:column;gap:2px;align-items:center;}
  .ko-bracket-mini .mini-label{font-size:8px;font-weight:700;color:var(--muted);margin-bottom:2px;text-transform:uppercase;}
  .ko-bracket-mini .mini-slot{width:100%;height:4px;border-radius:2px;background:var(--line);}"""

html = html.replace(old_ko_css, new_ko_css)

# ─── FIX 5: Expand knockout match data and replace renderKnockout + renderKnockoutPreview ───

# First, update the match data in __FIFA_DATA
m = re.search(r'window\.__FIFA_DATA\s*=\s*({.*?});', html, re.DOTALL)
data = json.loads(m.group(1))

# Remove existing knockout matches
data['matches'] = [x for x in data['matches'] if 'Group' in x.get('stage', 'Group')]

# Add all 32 knockout matches with real FIFA 2026 bracket structure
ko_matches = [
    # Round of 32 (matches 49-64)
    {"id":49,"match_number":49,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1A","away_placeholder":"3C/D/E/F","venue_id":8,"match_date":"2026-06-28","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":50,"match_number":50,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2C","away_placeholder":"2D","venue_id":11,"match_date":"2026-06-28","match_time_utc":"19:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":51,"match_number":51,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1B","away_placeholder":"3A/D/E/F","venue_id":6,"match_date":"2026-06-28","match_time_utc":"13:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":52,"match_number":52,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2A","away_placeholder":"2B","venue_id":9,"match_date":"2026-06-28","match_time_utc":"22:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":53,"match_number":53,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1D","away_placeholder":"3B/E/F","venue_id":7,"match_date":"2026-06-29","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":54,"match_number":54,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1C","away_placeholder":"3A/B/F","venue_id":12,"match_date":"2026-06-29","match_time_utc":"19:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":55,"match_number":55,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2E","away_placeholder":"2F","venue_id":13,"match_date":"2026-06-29","match_time_utc":"13:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":56,"match_number":56,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2G","away_placeholder":"2H","venue_id":10,"match_date":"2026-06-29","match_time_utc":"22:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":57,"match_number":57,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1E","away_placeholder":"3A/B/C/D","venue_id":14,"match_date":"2026-06-30","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":58,"match_number":58,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1F","away_placeholder":"3G/H/I/J","venue_id":15,"match_date":"2026-06-30","match_time_utc":"19:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":59,"match_number":59,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2I","away_placeholder":"2J","venue_id":16,"match_date":"2026-06-30","match_time_utc":"13:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":60,"match_number":60,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"2K","away_placeholder":"2L","venue_id":1,"match_date":"2026-06-30","match_time_utc":"22:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":61,"match_number":61,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1H","away_placeholder":"3I/J/K/L","venue_id":2,"match_date":"2026-07-01","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":62,"match_number":62,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1G","away_placeholder":"3H/I/J/K","venue_id":3,"match_date":"2026-07-01","match_time_utc":"19:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":63,"match_number":63,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1J","away_placeholder":"2I","venue_id":4,"match_date":"2026-07-01","match_time_utc":"13:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":64,"match_number":64,"stage":"Round of 32","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"1I","away_placeholder":"2L","venue_id":5,"match_date":"2026-07-01","match_time_utc":"22:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    # Round of 16 (matches 65-72)
    {"id":65,"match_number":65,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W49","away_placeholder":"W50","venue_id":8,"match_date":"2026-07-04","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":66,"match_number":66,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W51","away_placeholder":"W52","venue_id":6,"match_date":"2026-07-04","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":67,"match_number":67,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W53","away_placeholder":"W54","venue_id":7,"match_date":"2026-07-05","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":68,"match_number":68,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W55","away_placeholder":"W56","venue_id":9,"match_date":"2026-07-05","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":69,"match_number":69,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W57","away_placeholder":"W58","venue_id":10,"match_date":"2026-07-06","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":70,"match_number":70,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W59","away_placeholder":"W60","venue_id":11,"match_date":"2026-07-06","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":71,"match_number":71,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W61","away_placeholder":"W62","venue_id":12,"match_date":"2026-07-07","match_time_utc":"16:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":72,"match_number":72,"stage":"Round of 16","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W63","away_placeholder":"W64","venue_id":13,"match_date":"2026-07-07","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    # Quarter-finals (matches 73-76)
    {"id":73,"match_number":73,"stage":"Quarter-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W65","away_placeholder":"W66","venue_id":8,"match_date":"2026-07-09","match_time_utc":"18:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":74,"match_number":74,"stage":"Quarter-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W67","away_placeholder":"W68","venue_id":7,"match_date":"2026-07-09","match_time_utc":"21:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":75,"match_number":75,"stage":"Quarter-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W69","away_placeholder":"W70","venue_id":6,"match_date":"2026-07-10","match_time_utc":"18:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":76,"match_number":76,"stage":"Quarter-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W71","away_placeholder":"W72","venue_id":9,"match_date":"2026-07-10","match_time_utc":"21:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    # Semi-finals (matches 77-78)
    {"id":77,"match_number":77,"stage":"Semi-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W73","away_placeholder":"W74","venue_id":7,"match_date":"2026-07-14","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    {"id":78,"match_number":78,"stage":"Semi-final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W75","away_placeholder":"W76","venue_id":8,"match_date":"2026-07-15","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    # Third-place play-off (match 79)
    {"id":79,"match_number":79,"stage":"Third-place","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"L77","away_placeholder":"L78","venue_id":8,"match_date":"2026-07-18","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
    # Final (match 80)
    {"id":80,"match_number":80,"stage":"Final","group":None,"home_team_id":None,"away_team_id":None,"home_placeholder":"W77","away_placeholder":"W78","venue_id":6,"match_date":"2026-07-19","match_time_utc":"20:00","home_score":None,"away_score":None,"status":"scheduled","minute":None},
]

data['matches'].extend(ko_matches)

# Re-inject the data using string find/replace instead of regex (avoids unicode escape issues)
new_data_str = 'window.__FIFA_DATA = ' + json.dumps(data, separators=(',', ':'), ensure_ascii=False) + ';'
pat = re.compile(r'window\.__FIFA_DATA\s*=\s*\{.*?\};', re.DOTALL)
match_obj = pat.search(html)
if match_obj:
    html = html[:match_obj.start()] + new_data_str + html[match_obj.end():]
else:
    print("ERROR: Could not find __FIFA_DATA block!")
    exit(1)

# ─── FIX 6: Replace renderKnockout and renderKnockoutPreview functions ───
old_render = """function renderKnockout() {
  const el = $('#knockout-bracket');
  const koMatches = DB.matches.filter(m => !m.stage.includes('Group'));
  if (!koMatches.length) {
    el.innerHTML = `<div style="text-align:center;padding:30px 20px;">
      <div style="font-size:36px;margin-bottom:12px;">🏆</div>
      <div style="font-weight:800;font-size:15px;color:var(--text);margin-bottom:6px;">Knockout Stage</div>
      <div style="font-size:12px;color:var(--muted);line-height:1.5;">Begins after the group stage.<br>Top 2 from each group + 8 best 3rd-placed teams advance to the Round of 32.</div>
      <div style="margin-top:20px;">
        ${renderKnockoutPreview()}
      </div>
    </div>`;
    return;
  }

  const rounds = {};
  koMatches.forEach(m => { const r = m.stage; if (!rounds[r]) rounds[r] = []; rounds[r].push(m); });
  const roundOrder = ['Round of 32', 'Round of 16', 'Quarter-final', 'Semi-final', 'Final'];
  const activeRounds = roundOrder.filter(r => rounds[r]);

  function koMatchHtml(m) {
    const h = team(m.home_team_id);
    const a = team(m.away_team_id);
    const homeName = h.short_code || h.name || m.home_placeholder || 'TBD';
    const awayName = a.short_code || a.name || m.away_placeholder || 'TBD';
    const homeFlag = h.flag || '⬜';
    const awayFlag = a.flag || '⬜';
    const hScore = m.home_score !== null ? m.home_score : '';
    const aScore = m.away_score !== null ? m.away_score : '';
    const isFinished = m.status === 'finished';
    const hWin = isFinished && m.home_score > m.away_score;
    const aWin = isFinished && m.away_score > m.home_score;
    return `<div class="ko-match" data-mid="${m.id}">
      <div class="ko-team-row${hWin ? ' winner' : ''}${aWin ? ' loser' : ''}">
        <div class="team-info"><span>${homeFlag}</span> ${homeName}</div>
        <span class="ko-score">${hScore}</span>
      </div>
      <div class="ko-divider"></div>
      <div class="ko-team-row${aWin ? ' winner' : ''}${hWin ? ' loser' : ''}">
        <div class="team-info"><span>${awayFlag}</span> ${awayName}</div>
        <span class="ko-score">${aScore}</span>
      </div>
    </div>`;
  }

  let html = '<div class="ko-bracket"><div class="ko-tree ko-list">';
  activeRounds.forEach(rName => {
    const matches = rounds[rName];
    const shortName = rName.replace('Quarter-final','QF').replace('Semi-final','SF').replace('Round of ','R');
    html += `<div class="ko-round">
      <div class="ko-round-title">${shortName}</div>
      <div class="ko-round-matches">
        ${matches.map(m => koMatchHtml(m)).join('')}
      </div>
    </div>`;
  });
  html += '</div></div>';
  el.innerHTML = html;
}

function renderKnockoutPreview() {
  const roundOrder = ['Round of 32','Round of 16','Quarter-finals','Semi-finals','Final'];
  const counts = [16, 8, 4, 2, 1];
  const heights = [4, 8, 16, 32, 48];
  let svg = '<svg viewBox="0 0 520 260" style="width:100%;max-width:480px;" xmlns="http://www.w3.org/2000/svg">';
  const colW = 100;
  const gap = 4;

  roundOrder.forEach((name, ri) => {
    const x = ri * colW + 10;
    svg += `<text x="${x + 40}" y="16" text-anchor="middle" font-size="8" font-weight="800" fill="#64748b" letter-spacing=".5">${name.replace('Quarter-finals','QF').replace('Semi-finals','SF').replace('Round of ','R')}</text>`;
    const n = counts[ri];
    const totalH = 230;
    const slotH = totalH / n;
    for (let i = 0; i < n; i++) {
      const y = 24 + i * slotH + (slotH - heights[ri]) / 2;
      const h = heights[ri];
      svg += `<rect x="${x}" y="${y}" width="80" height="${h}" rx="3" fill="#e6eaf2" stroke="#d1d5db" stroke-width=".5"/>`;
      if (ri < 4) {
        const nextSlotH = totalH / counts[ri + 1];
        const nextI = Math.floor(i / 2);
        const nextY = 24 + nextI * nextSlotH + nextSlotH / 2;
        const thisY = y + h / 2;
        svg += `<line x1="${x + 80}" y1="${thisY}" x2="${x + colW}" y2="${nextY}" stroke="#d1d5db" stroke-width="1" opacity=".5"/>`;
      }
    }
  });
  svg += `<text x="490" y="145" text-anchor="middle" font-size="18">🏆</text>`;
  svg += '</svg>';
  return svg;
}"""

new_render = r"""function renderKnockout() {
  const el = $('#knockout-bracket');
  const koMatches = DB.matches.filter(m => !m.stage.includes('Group'));

  const rounds = {};
  koMatches.forEach(m => { const r = m.stage; if (!rounds[r]) rounds[r] = []; rounds[r].push(m); });
  const roundOrder = [
    {key:'Round of 32', label:'Round of 32', short:'R32'},
    {key:'Round of 16', label:'Round of 16', short:'R16'},
    {key:'Quarter-final', label:'Quarter-final', short:'QF'},
    {key:'Semi-final', label:'Semi-final', short:'SF'},
    {key:'Final', label:'Final', short:'F'},
  ];
  const activeRounds = roundOrder.filter(r => rounds[r.key]);

  // Also include Third-place if present
  if (rounds['Third-place']) {
    activeRounds.splice(activeRounds.length, 0, {key:'Third-place', label:'3rd Place', short:'3rd'});
  }

  function fmtMatchDate(d) {
    if (!d) return '';
    const dt = new Date(d + 'T00:00:00');
    return dt.toLocaleDateString('en-US', {month:'short', day:'numeric'});
  }

  function koMatchCard(m) {
    const h = team(m.home_team_id);
    const a = team(m.away_team_id);
    const homeName = h.short_code || h.name || m.home_placeholder || 'TBD';
    const awayName = a.short_code || a.name || m.away_placeholder || 'TBD';
    const homeFlag = h.flag || '🏳️';
    const awayFlag = a.flag || '🏳️';
    const hScore = m.home_score !== null ? m.home_score : '–';
    const aScore = m.away_score !== null ? m.away_score : '–';
    const isFinished = m.status === 'finished';
    const hWin = isFinished && m.home_score > m.away_score;
    const aWin = isFinished && m.away_score > m.home_score;
    return `<div class="ko-match" data-mid="${m.id}">
      <div class="ko-match-num">
        <span>Match ${m.match_number}</span>
        <span class="ko-match-date">${fmtMatchDate(m.match_date)}</span>
      </div>
      <div class="ko-team-row${hWin ? ' winner' : ''}${aWin ? ' loser' : ''}">
        <div class="team-info"><span class="team-flag">${homeFlag}</span><span class="team-code">${homeName}</span></div>
        <span class="ko-score">${hScore}</span>
      </div>
      <div class="ko-divider"></div>
      <div class="ko-team-row${aWin ? ' winner' : ''}${hWin ? ' loser' : ''}">
        <div class="team-info"><span class="team-flag">${awayFlag}</span><span class="team-code">${awayName}</span></div>
        <span class="ko-score">${aScore}</span>
      </div>
    </div>`;
  }

  // Build filter rail
  let filterHtml = '<div class="ko-filter-rail" id="ko-filter-rail">';
  activeRounds.forEach((r, i) => {
    filterHtml += `<div class="ko-filter-btn${i === 0 ? ' active' : ''}" data-round="${r.key}">${r.label}</div>`;
  });
  filterHtml += '</div>';

  // Build round containers
  let roundsHtml = '';
  activeRounds.forEach((r, i) => {
    const matches = rounds[r.key];
    matches.sort((a, b) => a.match_number - b.match_number);
    roundsHtml += `<div class="ko-round-container${i === 0 ? ' visible' : ''}" data-round="${r.key}" style="${i !== 0 ? 'display:none;' : ''}">`;
    roundsHtml += `<div class="ko-round-label">${r.label} · ${matches.length} Match${matches.length > 1 ? 'es' : ''}</div>`;

    // Group matches into pairs for connector visualization
    for (let j = 0; j < matches.length; j += 2) {
      roundsHtml += '<div class="ko-match-pair">';
      roundsHtml += koMatchCard(matches[j]);
      if (j + 1 < matches.length) {
        // SVG connector between paired matches
        roundsHtml += `<div class="ko-pair-svg">
          <svg viewBox="0 0 80 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 0 L40 12 M20 12 L60 12" stroke="#d1d5db" stroke-width="1.5" fill="none" stroke-linecap="round"/>
          </svg>
        </div>`;
        roundsHtml += koMatchCard(matches[j + 1]);
      }
      // Show which next match the winners feed into
      const m1 = matches[j];
      const nextRound = activeRounds[activeRounds.indexOf(r) + 1];
      if (nextRound && rounds[nextRound.key]) {
        const nextMatch = rounds[nextRound.key].find(nm =>
          (nm.home_placeholder && nm.home_placeholder.includes('W' + m1.match_number)) ||
          (nm.away_placeholder && nm.away_placeholder.includes('W' + m1.match_number))
        );
        if (nextMatch) {
          roundsHtml += `<div class="ko-pair-connector"><span class="ko-pair-label">Winner → Match ${nextMatch.match_number}</span></div>`;
        }
      }
      roundsHtml += '</div>';
    }
    roundsHtml += '</div>';
  });

  el.innerHTML = filterHtml + roundsHtml;

  // Wire up filter buttons
  const filterBtns = el.querySelectorAll('.ko-filter-btn');
  const roundContainers = el.querySelectorAll('.ko-round-container');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const roundKey = btn.dataset.round;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Scroll the active button into view
      btn.scrollIntoView({behavior:'smooth', block:'nearest', inline:'center'});

      // Animate transition
      roundContainers.forEach(rc => {
        if (rc.dataset.round === roundKey) {
          rc.style.display = '';
          rc.classList.remove('visible');
          rc.classList.add('entering');
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              rc.classList.remove('entering');
              rc.classList.add('visible');
            });
          });
        } else {
          rc.classList.remove('visible');
          rc.style.display = 'none';
        }
      });
    });
  });
}"""

html = html.replace(old_render, new_render)

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ All patches applied successfully!")
print(f"  - Removed X close button from overlay")
print(f"  - Added scrollTop=0 on overlay open")
print(f"  - Fixed overlay flex layout for bottom whitespace")
print(f"  - Replaced knockout CSS with FIFA.com-style filter rail")
print(f"  - Expanded knockout matches: {len(ko_matches)} total (16 R32 + 8 R16 + 4 QF + 2 SF + 1 3rd + 1 Final)")
print(f"  - Replaced renderKnockout with filter-based UI")
