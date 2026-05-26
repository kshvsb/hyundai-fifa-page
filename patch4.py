#!/usr/bin/env python3
"""Patch 4: Rebuild knockout bracket as FIFA.com tree layout with connecting lines."""

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# ─── 1. REPLACE ALL KNOCKOUT CSS ───
old_ko_css = """  /* Knockout bracket — FIFA.com style with round filters */
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
    padding:8px 16px 16px;
    opacity:0;transform:translateY(12px);
    transition:opacity .4s cubic-bezier(.3,0,.15,1),transform .4s cubic-bezier(.3,0,.15,1);
  }
  .ko-round-container.visible{opacity:1;transform:translateY(0);}
  .ko-round-container.hidden{display:none;}
  .ko-round-label{
    font-size:11px;font-weight:800;color:var(--hyundai-accent);text-transform:uppercase;
    letter-spacing:.8px;margin-bottom:10px;text-align:center;
  }
  .ko-match-pair{margin-bottom:10px;}
  .ko-pair-connector{
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4px 0 8px;
  }
  .ko-pair-label{font-size:9px;color:var(--hyundai-accent);font-weight:700;letter-spacing:.5px;}
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
  .ko-pair-svg{text-align:center;margin:2px 0 -2px;}
  .ko-pair-svg svg{width:100px;height:32px;}
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

new_ko_css = """  /* Knockout bracket — FIFA.com tree layout */
  .ko-filter-rail{
    display:flex;gap:8px;padding:12px 16px 10px;overflow-x:auto;scrollbar-width:none;
    background:var(--bg);position:sticky;top:0;z-index:5;
  }
  .ko-filter-rail::-webkit-scrollbar{display:none;}
  .ko-filter-btn{
    padding:10px 18px;border-radius:24px;font-size:12px;font-weight:600;
    color:var(--text);background:#fff;border:1.5px solid var(--line);white-space:nowrap;
    cursor:pointer;transition:all .2s ease;flex-shrink:0;
  }
  .ko-filter-btn:active{transform:scale(.95);}
  .ko-filter-btn.active{
    background:var(--text);color:#fff;border-color:var(--text);
  }

  /* Tree bracket container — horizontally scrollable */
  .ko-tree-wrap{
    overflow-x:auto;overflow-y:visible;padding:8px 0 20px;scrollbar-width:none;
    -webkit-overflow-scrolling:touch;
  }
  .ko-tree-wrap::-webkit-scrollbar{display:none;}
  .ko-tree{
    display:flex;align-items:stretch;min-width:max-content;position:relative;gap:0;
  }

  /* Each round column */
  .ko-col{
    display:flex;flex-direction:column;justify-content:space-around;
    min-width:160px;position:relative;padding:0 4px;
  }

  /* Bracket section: 2 feeder matches + 1 destination match */
  .ko-bracket-section{
    position:relative;margin-bottom:24px;
  }
  .ko-bracket-pair{
    display:flex;align-items:stretch;gap:0;
  }
  .ko-feeder{
    display:flex;flex-direction:column;justify-content:center;gap:8px;
    min-width:160px;position:relative;
  }
  .ko-connector{
    position:relative;width:28px;display:flex;flex-direction:column;justify-content:center;flex-shrink:0;
  }
  .ko-dest{
    display:flex;flex-direction:column;justify-content:center;
    min-width:160px;
  }

  /* Match card */
  .ko-match{
    background:#fff;border-radius:8px;border:1px solid #d5d8dc;
    cursor:pointer;position:relative;overflow:hidden;
    transition:transform .15s,box-shadow .15s;
  }
  .ko-match:active{transform:scale(.97);box-shadow:0 1px 3px rgba(0,0,0,.08);}
  .ko-match-header{
    display:flex;align-items:center;gap:6px;padding:0 0 4px;
  }
  .ko-match-id{
    font-size:10px;font-weight:700;color:var(--muted);
  }
  .ko-match-date{
    font-size:10px;color:var(--muted);font-weight:400;margin-bottom:4px;
  }
  .ko-team-row{
    display:flex;align-items:center;justify-content:space-between;
    padding:6px 10px;background:#fff;
  }
  .ko-team-row:first-of-type{border-bottom:1px solid #eee;}
  .ko-team-row .team-info{
    display:flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--text);
  }
  .ko-team-row .team-info .team-flag{
    width:24px;height:16px;display:flex;align-items:center;justify-content:center;
    background:#f0f2f7;border-radius:2px;font-size:12px;line-height:1;
  }
  .ko-team-row .team-info .team-code{font-size:13px;}
  .ko-team-row .ko-score{font-size:13px;font-weight:700;color:var(--text);min-width:16px;text-align:center;}
  .ko-team-row.winner .team-info{font-weight:700;}
  .ko-team-row.loser{opacity:.4;}
  .ko-divider{display:none;}

  /* Round container for filtered view */
  .ko-round-container{padding:0 12px 16px;}
  .ko-round-container.hidden{display:none;}
  .ko-round-container.visible{display:block;}"""

html = html.replace(old_ko_css, new_ko_css)

# ─── 2. REPLACE renderKnockout FUNCTION ───
old_render_start = "function renderKnockout() {"
old_render_end = """    });
  });
}

function openMatchDetail(matchId) {"""

# Find and replace the entire renderKnockout function
import re
pattern = re.compile(r'function renderKnockout\(\)\s*\{.*?\n\}\n\nfunction openMatchDetail', re.DOTALL)
match = pattern.search(html)
if not match:
    print("ERROR: Could not find renderKnockout function!")
    exit(1)

new_render = r"""function renderKnockout() {
  const el = $('#knockout-bracket');
  const koMatches = DB.matches.filter(m => !m.stage.includes('Group'));
  const rounds = {};
  koMatches.forEach(m => { const r = m.stage; if (!rounds[r]) rounds[r] = []; rounds[r].push(m); });

  const roundDefs = [
    {key:'Round of 32', label:'Round of 32'},
    {key:'Round of 16', label:'Round of 16'},
    {key:'Quarter-final', label:'Quarter-final'},
    {key:'Semi-final', label:'Semi-final'},
    {key:'Final', label:'Final'},
    {key:'Third-place', label:'3rd Place'},
  ];
  const activeRounds = roundDefs.filter(r => rounds[r.key]);

  function fmtKoDate(d, t) {
    if (!d) return '';
    const [y,mo,da] = d.split('-');
    return `${mo}/${da}/${y}` + (t ? `    ${t}` : '');
  }

  function matchCard(m, showDate) {
    const h = team(m.home_team_id);
    const a = team(m.away_team_id);
    const homeName = h.short_code || m.home_placeholder || 'TBD';
    const awayName = a.short_code || m.away_placeholder || 'TBD';
    const homeFlag = h.flag || '';
    const awayFlag = a.flag || '';
    const isFinished = m.status === 'finished';
    const hWin = isFinished && m.home_score > m.away_score;
    const aWin = isFinished && m.away_score > m.home_score;
    const dateStr = showDate !== false ? fmtKoDate(m.match_date, m.match_time_utc) : '';
    return `${dateStr ? `<div class="ko-match-date">${dateStr}</div>` : ''}
    <div class="ko-match" data-mid="${m.id}">
      <div class="ko-team-row${hWin ? ' winner' : ''}${aWin ? ' loser' : ''}">
        <div class="team-info"><span class="team-flag">${homeFlag || '&nbsp;'}</span><span class="team-code">${homeName}</span></div>
      </div>
      <div class="ko-team-row${aWin ? ' winner' : ''}${hWin ? ' loser' : ''}">
        <div class="team-info"><span class="team-flag">${awayFlag || '&nbsp;'}</span><span class="team-code">${awayName}</span></div>
      </div>
    </div>`;
  }

  // Build a bracket-tree view for each filtered round
  // When R32 is selected: show pairs of R32 matches feeding into R16 matches
  // When R16 is selected: show pairs of R16 matches feeding into QF matches
  // etc.

  function buildBracketPairs(roundKey) {
    const matches = (rounds[roundKey] || []).sort((a,b) => a.match_number - b.match_number);
    // Find the next round
    const nextRoundIdx = roundDefs.findIndex(r => r.key === roundKey) + 1;
    const nextRoundKey = nextRoundIdx < roundDefs.length ? roundDefs[nextRoundIdx].key : null;
    const nextMatches = nextRoundKey ? (rounds[nextRoundKey] || []) : [];

    let html = '<div class="ko-tree-wrap"><div class="ko-tree">';

    // Group into pairs
    for (let i = 0; i < matches.length; i += 2) {
      const m1 = matches[i];
      const m2 = matches[i + 1];

      // Find destination match in next round
      let destMatch = null;
      if (m1 && nextMatches.length) {
        destMatch = nextMatches.find(nm =>
          (nm.home_placeholder && (nm.home_placeholder === 'W' + m1.match_number)) ||
          (nm.away_placeholder && (nm.away_placeholder === 'W' + m1.match_number))
        );
      }

      html += '<div class="ko-bracket-section"><div class="ko-bracket-pair">';

      // Left column: feeder matches
      html += '<div class="ko-feeder">';
      html += `<div style="margin-bottom:4px;">
        <div class="ko-match-id">M${m1.match_number}</div>
        ${matchCard(m1)}
      </div>`;
      if (m2) {
        html += `<div style="margin-top:4px;">
          <div class="ko-match-id">M${m2.match_number}</div>
          ${matchCard(m2)}
        </div>`;
      }
      html += '</div>';

      // Connector lines (SVG)
      if (destMatch && m2) {
        html += `<div class="ko-connector">
          <svg width="28" height="100%" viewBox="0 0 28 200" preserveAspectRatio="none" style="width:28px;height:100%;">
            <line x1="0" y1="50" x2="14" y2="50" stroke="#bcc3cf" stroke-width="1.5"/>
            <line x1="14" y1="50" x2="14" y2="150" stroke="#bcc3cf" stroke-width="1.5"/>
            <line x1="0" y1="150" x2="14" y2="150" stroke="#bcc3cf" stroke-width="1.5"/>
            <line x1="14" y1="100" x2="28" y2="100" stroke="#bcc3cf" stroke-width="1.5"/>
          </svg>
        </div>`;

        // Right column: destination match
        html += '<div class="ko-dest">';
        html += `<div class="ko-match-id">M${destMatch.match_number}</div>`;
        html += matchCard(destMatch);
        html += '</div>';
      }

      html += '</div></div>';
    }

    html += '</div></div>';
    return html;
  }

  // For Final and 3rd place, just show the single match
  function buildSingleRound(roundKey) {
    const matches = (rounds[roundKey] || []).sort((a,b) => a.match_number - b.match_number);
    let html = '<div style="padding:12px 16px;">';
    matches.forEach(m => {
      html += `<div style="margin-bottom:16px;">
        <div class="ko-match-id">M${m.match_number}</div>
        ${matchCard(m)}
      </div>`;
    });
    html += '</div>';
    return html;
  }

  // Build filter rail
  let filterHtml = '<div class="ko-filter-rail">';
  activeRounds.forEach((r, i) => {
    filterHtml += `<div class="ko-filter-btn${i === 0 ? ' active' : ''}" data-round="${r.key}">${r.label}</div>`;
  });
  filterHtml += '</div>';

  // Build round containers
  let roundsHtml = '';
  activeRounds.forEach((r, i) => {
    const isSingle = r.key === 'Final' || r.key === 'Third-place';
    const content = isSingle ? buildSingleRound(r.key) : buildBracketPairs(r.key);
    roundsHtml += `<div class="ko-round-container${i === 0 ? ' visible' : ' hidden'}" data-round="${r.key}">
      ${content}
    </div>`;
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
      btn.scrollIntoView({behavior:'smooth', block:'nearest', inline:'center'});
      roundContainers.forEach(rc => {
        if (rc.dataset.round === roundKey) {
          rc.classList.remove('hidden');
          rc.classList.add('visible');
        } else {
          rc.classList.remove('visible');
          rc.classList.add('hidden');
        }
      });
    });
  });
}

function openMatchDetail(matchId) {"""

html = html[:match.start()] + new_render + html[match.end():]

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ Patch 4 applied: Knockout bracket rebuilt as FIFA.com tree layout")
print("  - Bracket pairs: 2 feeder matches → connector lines → destination match")
print("  - SVG bracket connector lines between paired matches")
print("  - Match number labels (M49, M50, M65)")
print("  - Date/time above each match card")
print("  - Horizontally scrollable tree view")
print("  - Filter buttons styled like FIFA.com (dark fill)")
print("  - Click any match card to open match detail")
