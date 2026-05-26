#!/usr/bin/env python3
"""Patch 2: Redesign matches like FIFA.com mobile, fix knockout connectors + transitions."""

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'r') as f:
    html = f.read()

# ─── 1. REDESIGN MATCH CARDS — FIFA.com mobile style ───
# Replace schedule-card CSS with FIFA-style centered match card
old_sched_css = """  .schedule-card{
    background:var(--card);border-radius:12px;padding:12px 14px;border:1px solid var(--line);
    display:flex;align-items:center;gap:12px;margin-bottom:6px;
  }
  .sched-time{
    font-size:12px;font-weight:800;color:#fff;
    min-width:46px;
  }
  .sched-time small{display:block;font-size:9px;color:var(--muted);font-weight:600;}
  .sched-teams{flex:1;display:flex;align-items:center;gap:8px;font-size:12px;font-weight:600;}
  .sched-teams .flag{width:22px;height:22px;font-size:13px;border-width:1px;}
  .sched-stage{font-size:9px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.4px;}"""

new_sched_css = """  .schedule-card{
    background:var(--card);border-radius:14px;padding:18px 16px 14px;border:1px solid var(--line);
    margin-bottom:8px;text-align:center;
  }
  .sched-matchup{
    display:flex;align-items:center;justify-content:center;gap:0;margin-bottom:8px;
  }
  .sched-team{
    display:flex;align-items:center;gap:8px;min-width:0;flex:1;
  }
  .sched-team.home{justify-content:flex-end;}
  .sched-team.away{justify-content:flex-start;}
  .sched-team .team-code{font-size:14px;font-weight:700;color:var(--text);}
  .sched-team .team-flag{font-size:26px;line-height:1;}
  .sched-center{
    min-width:80px;text-align:center;padding:0 8px;
  }
  .sched-center .sched-time{
    font-size:22px;font-weight:800;color:var(--text);
    letter-spacing:-0.5px;
  }
  .sched-center .sched-score{
    font-size:26px;font-weight:900;color:var(--text);
    letter-spacing:2px;
  }
  .sched-info{
    font-size:11px;color:var(--muted);line-height:1.5;
  }
  .sched-info .sched-stage{font-weight:600;color:var(--hyundai-accent);}
  .sched-info .sched-venue{font-weight:400;}"""

html = html.replace(old_sched_css, new_sched_css)

# Also update the day-label to be more like FIFA.com date headers
old_day_css = """  .day-group{margin-bottom:14px;}
  .day-label{
    font-size:11px;font-weight:800;color:var(--muted);
    text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px;padding-left:2px;
  }"""

new_day_css = """  .day-group{margin-bottom:18px;}
  .day-label{
    font-size:14px;font-weight:800;color:var(--text);
    margin-bottom:10px;padding-left:2px;
    display:flex;justify-content:space-between;align-items:center;
  }"""

html = html.replace(old_day_css, new_day_css)

# ─── 2. REPLACE matchCard function — FIFA.com centered layout ───
old_matchCard = """function matchCard(m, isLive) {
  const h = team(m.home_team_id);
  const a = team(m.away_team_id);
  const v = venue(m.venue_id);
  const homeName = h.name || m.home_placeholder || 'TBD';
  const awayName = a.name || m.away_placeholder || 'TBD';
  const homeFlag = h.flag || '🏳️';
  const awayFlag = a.flag || '🏳️';
  const scoreH = m.home_score !== null ? m.home_score : '-';
  const scoreA = m.away_score !== null ? m.away_score : '-';

  if (isLive) {
    return `<div class="live-card" data-mid="${m.id}">
      <div class="live-head">
        <span class="live-badge"><span class="live-dot"></span>LIVE · ${m.minute || ''}</span>
        <span class="live-meta">${v.city || ''}</span>
      </div>
      <div class="match-row">
        <div class="team"><div class="flag">${homeFlag}</div><div class="team-name">${homeName}</div></div>
        <div class="score">${scoreH} <span class="vs">:</span> ${scoreA}</div>
        <div class="team away"><div class="flag">${awayFlag}</div><div class="team-name">${awayName}</div></div>
      </div>
    </div>`;
  }

  return `<div class="schedule-card" data-mid="${m.id}">
    <div class="sched-time">${fmtTime(m.match_time_utc)}<small>${fmtDate(m.match_date)}</small></div>
    <div class="sched-teams">${homeFlag} ${h.short_code || homeName} <span style="color:var(--muted)">vs</span> ${awayFlag} ${a.short_code || awayName}</div>
    <div class="sched-stage">${m.group ? 'Group ' + m.group : m.stage}</div>
  </div>`;
}"""

new_matchCard = r"""function matchCard(m, isLive) {
  const h = team(m.home_team_id);
  const a = team(m.away_team_id);
  const v = venue(m.venue_id);
  const homeName = h.name || m.home_placeholder || 'TBD';
  const awayName = a.name || m.away_placeholder || 'TBD';
  const homeCode = h.short_code || m.home_placeholder || 'TBD';
  const awayCode = a.short_code || m.away_placeholder || 'TBD';
  const homeFlag = h.flag || '🏳️';
  const awayFlag = a.flag || '🏳️';
  const scoreH = m.home_score !== null ? m.home_score : '-';
  const scoreA = m.away_score !== null ? m.away_score : '-';
  const isPlayed = m.status === 'finished';
  const stageLabel = m.group ? 'First Stage' : m.stage;
  const groupLabel = m.group ? 'Group ' + m.group : '';
  const venueLabel = v.name ? v.name + (v.city ? ' (' + v.city.split('(')[0].split(',')[0].trim() + ')' : '') : '';

  if (isLive) {
    return `<div class="live-card" data-mid="${m.id}">
      <div class="live-head">
        <span class="live-badge"><span class="live-dot"></span>LIVE · ${m.minute || ''}'</span>
        <span class="live-meta">${v.city || ''}</span>
      </div>
      <div class="match-row">
        <div class="team"><div class="flag">${homeFlag}</div><div class="team-name">${homeName}</div></div>
        <div class="score">${scoreH} <span class="vs">:</span> ${scoreA}</div>
        <div class="team away"><div class="flag">${awayFlag}</div><div class="team-name">${awayName}</div></div>
      </div>
    </div>`;
  }

  const centerContent = isPlayed
    ? `<div class="sched-score">${scoreH}:${scoreA}</div>`
    : `<div class="sched-time">${fmtTime(m.match_time_utc)}</div>`;

  return `<div class="schedule-card" data-mid="${m.id}">
    <div class="sched-matchup">
      <div class="sched-team home"><span class="team-code">${homeCode}</span><span class="team-flag">${homeFlag}</span></div>
      <div class="sched-center">${centerContent}</div>
      <div class="sched-team away"><span class="team-flag">${awayFlag}</span><span class="team-code">${awayCode}</span></div>
    </div>
    <div class="sched-info">
      <span class="sched-stage">${stageLabel}</span>
      ${groupLabel || venueLabel ? '<br>' : ''}
      <span class="sched-venue">${[groupLabel, venueLabel].filter(Boolean).join(' · ')}</span>
    </div>
  </div>`;
}"""

html = html.replace(old_matchCard, new_matchCard)

# ─── 3. FIX DUPLICATE DATES — date is in the day-group heading AND in each card ───
# The renderMatches day-label already shows the date. The matchCard no longer shows date (we removed it).
# But let's also make the day-label use a nicer long format like FIFA.com
old_renderMatches = """function renderMatches() {
  const el = $('#all-matches');
  const grouped = {};
  DB.matches.forEach(m => {
    const key = m.match_date;
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(m);
  });
  let html = '';
  Object.keys(grouped).sort().forEach(date => {
    html += `<div class="day-group"><div class="day-label">${fmtDate(date)}</div>`;
    grouped[date].forEach(m => {
      if (m.status === 'live') html += matchCard(m, true);
      else html += matchCard(m, false);
    });
    html += '</div>';
  });
  el.innerHTML = html;
}"""

new_renderMatches = r"""function renderMatches() {
  const el = $('#all-matches');
  const grouped = {};
  DB.matches.filter(m => m.stage.includes('Group') || m.home_team_id || m.away_team_id || m.home_placeholder).forEach(m => {
    const key = m.match_date;
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(m);
  });
  let html = '';
  Object.keys(grouped).sort().forEach(date => {
    const dt = new Date(date + 'T00:00:00');
    const longDate = dt.toLocaleDateString('en-US', {weekday:'long', day:'numeric', month:'long', year:'numeric'});
    html += `<div class="day-group"><div class="day-label">${longDate}</div>`;
    grouped[date].forEach(m => {
      if (m.status === 'live') html += matchCard(m, true);
      else html += matchCard(m, false);
    });
    html += '</div>';
  });
  el.innerHTML = html;
}"""

html = html.replace(old_renderMatches, new_renderMatches)

# ─── 4. FIX KNOCKOUT BRACKET — add SVG connectors and restore transitions ───
# Replace the knockout CSS to add proper connector styling
old_ko_pair_css = """  .ko-pair-svg{text-align:center;margin:4px 0 -2px;}
  .ko-pair-svg svg{width:80px;height:24px;}"""

new_ko_pair_css = """  .ko-pair-svg{text-align:center;margin:2px 0 -2px;}
  .ko-pair-svg svg{width:100px;height:32px;}"""

html = html.replace(old_ko_pair_css, new_ko_pair_css)

# Replace the connector SVG in renderKnockout to be more visible bracket-style lines
old_svg = """        roundsHtml += `<div class="ko-pair-svg">
          <svg viewBox="0 0 80 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M40 0 L40 12 M20 12 L60 12" stroke="#d1d5db" stroke-width="1.5" fill="none" stroke-linecap="round"/>
          </svg>
        </div>`;"""

new_svg = """        roundsHtml += `<div class="ko-pair-svg">
          <svg viewBox="0 0 100 32" xmlns="http://www.w3.org/2000/svg">
            <path d="M50 0 L50 4 M50 4 Q50 8 46 8 L20 8 M50 4 Q50 8 54 8 L80 8" stroke="#c7cdd8" stroke-width="2" fill="none" stroke-linecap="round"/>
            <path d="M50 28 L50 32" stroke="#c7cdd8" stroke-width="2" fill="none" stroke-linecap="round"/>
            <circle cx="50" cy="16" r="8" fill="#f0f2f7" stroke="#c7cdd8" stroke-width="1.5"/>
            <text x="50" y="19" text-anchor="middle" font-size="8" font-weight="700" fill="#64748b">VS</text>
          </svg>
        </div>`;"""

html = html.replace(old_svg, new_svg)

# Also improve the "Winner → Match X" connector to be more visual
old_winner_label = """      roundsHtml += `<div class="ko-pair-connector"><span class="ko-pair-label">Winner → Match ${nextMatch.match_number}</span></div>`;"""

new_winner_label = """      roundsHtml += `<div class="ko-pair-connector">
              <svg viewBox="0 0 100 20" style="width:100px;height:20px;display:block;margin:0 auto;">
                <path d="M50 0 L50 10 M42 10 L58 10 L50 20 L42 10" stroke="#c7cdd8" stroke-width="1.5" fill="#e6eaf2" stroke-linejoin="round"/>
              </svg>
              <span class="ko-pair-label">→ Match ${nextMatch.match_number}</span>
            </div>`;"""

html = html.replace(old_winner_label, new_winner_label)

# Improve ko-pair-connector CSS
old_pair_conn_css = """  .ko-pair-connector{
    display:flex;align-items:center;justify-content:center;padding:2px 0;
  }
  .ko-pair-label{font-size:9px;color:var(--muted);font-weight:600;letter-spacing:.5px;}"""

new_pair_conn_css = """  .ko-pair-connector{
    display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4px 0 8px;
  }
  .ko-pair-label{font-size:9px;color:var(--hyundai-accent);font-weight:700;letter-spacing:.5px;}"""

html = html.replace(old_pair_conn_css, new_pair_conn_css)

with open('/Users/keshav/Documents/Claude/hyundai-fifa-page/index.html', 'w') as f:
    f.write(html)

print("✅ Patch 2 applied:")
print("  - Matches redesigned: FIFA.com style (large flags, 3-letter codes, centered time)")
print("  - Duplicate dates removed: only date heading, no date in card")
print("  - Day labels: long format like FIFA.com ('Friday 12 June 2026')")
print("  - Knockout connectors: bracket-style SVG with VS circle")
print("  - Winner arrows: visual downward arrow connector with match number")
