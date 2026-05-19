import re

with open('dashboard.html', 'r') as f:
    html = f.read()

# 1. Update KPI Charts
kpi_blue = r'<svg viewBox="0 0 100 20".*?</svg>'
new_kpi_blue = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 15 Q 15 5, 25 15 T 50 15 T 75 25 T 100 10" fill="none" stroke="#3b82f6" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-icon blue">.*?</div>\s*</div>\s*<div class="kpi-value">24,842</div>\s*<div class="kpi-trend">.*?</div>\s*<div class="kpi-chart">\s*<svg.*?</svg>\s*</div>', 
              r'<div class="kpi-icon blue"><svg viewBox="0 0 24 24" width="10" height="10"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg></div>\n          </div>\n          <div class="kpi-value">24,842</div>\n          <div class="kpi-trend"><span class="trend-up" style="color:var(--success)">↑ 28.5%</span> vs last 6h</div>\n          <div class="kpi-chart">\n            ' + new_kpi_blue + '\n          </div>', html, flags=re.DOTALL)

new_kpi_purple = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 15 L 20 15 Q 35 15, 45 10 T 65 15 T 85 20 T 100 15" fill="none" stroke="#8b5cf6" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-icon purple">.*?</div>\s*</div>\s*<div class="kpi-value">1,243</div>\s*<div class="kpi-trend">.*?</div>\s*<div class="kpi-chart">\s*<svg.*?</svg>\s*</div>', 
              r'<div class="kpi-icon purple"><svg viewBox="0 0 24 24" width="10" height="10"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>\n          </div>\n          <div class="kpi-value">1,243</div>\n          <div class="kpi-trend"><span class="trend-up" style="color:var(--purple)">↑ 15.7%</span> vs last 6h</div>\n          <div class="kpi-chart">\n            ' + new_kpi_purple + '\n          </div>', html, flags=re.DOTALL)

new_kpi_amber = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 18 Q 15 18, 25 15 T 45 15 T 65 20 T 85 10 T 100 18" fill="none" stroke="#f59e0b" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-icon amber">.*?</div>\s*</div>\s*<div class="kpi-value">327</div>\s*<div class="kpi-trend">.*?</div>\s*<div class="kpi-chart">\s*<svg.*?</svg>\s*</div>', 
              r'<div class="kpi-icon amber"><svg viewBox="0 0 24 24" width="10" height="10"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>\n          </div>\n          <div class="kpi-value">327</div>\n          <div class="kpi-trend"><span class="trend-up" style="color:var(--warning)">↑ 18.3%</span> vs last 6h</div>\n          <div class="kpi-chart">\n            ' + new_kpi_amber + '\n          </div>', html, flags=re.DOTALL)

new_kpi_green = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 15 L 30 15 Q 45 15, 55 12 T 75 15 T 95 18 T 100 10" fill="none" stroke="#10b981" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-icon green">.*?</div>\s*</div>\s*<div class="kpi-value">99\.98%</div>\s*<div class="kpi-trend">.*?</div>\s*<div class="kpi-chart">\s*<svg.*?</svg>\s*</div>', 
              r'<div class="kpi-icon green"><svg viewBox="0 0 24 24" width="10" height="10"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div>\n          </div>\n          <div class="kpi-value">99.98%</div>\n          <div class="kpi-trend"><span class="trend-up" style="color:var(--success)">↑ 0.02%</span> vs last 6h</div>\n          <div class="kpi-chart">\n            ' + new_kpi_green + '\n          </div>', html, flags=re.DOTALL)

new_kpi_yellow = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 10 Q 15 10, 25 10 T 45 10 T 65 20 T 85 10 T 100 12" fill="none" stroke="#facc15" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-icon yellow">.*?</div>\s*</div>\s*<div class="kpi-value">\$1,842\.77</div>\s*<div class="kpi-trend">.*?</div>\s*<div class="kpi-chart">\s*<svg.*?</svg>\s*</div>', 
              r'<div class="kpi-icon yellow"><svg viewBox="0 0 24 24" width="10" height="10"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg></div>\n          </div>\n          <div class="kpi-value">$1,842.77</div>\n          <div class="kpi-trend"><span class="trend-down" style="color:var(--danger)">↓ 8.4%</span> vs last 6h</div>\n          <div class="kpi-chart">\n            ' + new_kpi_yellow + '\n          </div>', html, flags=re.DOTALL)

# 2. Update Middle Area Line Charts
# Throughput graph exact bezier
throughput_path = "M0 75 Q 5 70, 10 75 T 25 45 T 40 85 T 50 25 T 60 90 T 70 5 T 80 95 T 90 20 T 95 90 T 100 40"
throughput_svg = f"""<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:100%; overflow:visible;">
                <defs>
                  <linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3"/>
                    <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0"/>
                  </linearGradient>
                  <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>
                <path d="{throughput_path}" fill="none" stroke="#3b82f6" stroke-width="2.5" filter="url(#glowBlue)" vector-effect="non-scaling-stroke"/>
                <path d="{throughput_path} L 100 100 L 0 100 Z" fill="url(#blueGrad)" stroke="none"/>
                <!-- grid lines -->
                <line x1="0" y1="25" x2="100" y2="25" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
                <line x1="0" y1="50" x2="100" y2="50" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
                <line x1="0" y1="75" x2="100" y2="75" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
              </svg>"""

html = re.sub(r'<div class="chart-area">\s*<svg.*?</svg>\s*</div>', r'<div class="chart-area">\n              ' + throughput_svg + '\n            </div>', html, count=1, flags=re.DOTALL)

# Latency graph exact jagged
latency_path = "M0 70 L 5 60 L 10 50 L 15 65 L 20 40 L 25 50 L 30 65 L 35 45 L 40 60 L 45 40 L 50 60 L 55 50 L 60 70 L 65 50 L 70 65 L 75 45 L 80 65 L 85 45 L 90 60 L 95 40 L 100 50"
latency_svg = f"""<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:100%; overflow:visible;">
                <defs>
                  <filter id="glowPurple" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="1.5" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                </defs>
                <path d="{latency_path}" fill="none" stroke="#8b5cf6" stroke-width="2.5" filter="url(#glowPurple)" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>
                <line x1="0" y1="25" x2="100" y2="25" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
                <line x1="0" y1="50" x2="100" y2="50" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
                <line x1="0" y1="75" x2="100" y2="75" stroke="#1f2937" stroke-width="1" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>
              </svg>"""

html = re.sub(r'<div class="chart-area">\s*<svg.*?</svg>\s*</div>', r'<div class="chart-area">\n              ' + latency_svg + '\n            </div>', html, count=1, flags=re.DOTALL)


# 3. Donut Legend alignment
html = html.replace('justify-content: space-between;', 'justify-content: flex-start;')
html = html.replace('<div class="donut-legend-val">', '<div class="donut-legend-val" style="margin-left:auto;">')
html = html.replace('<div class="donut-legend-val" style="color:var(--warning)">', '<div class="donut-legend-val" style="margin-left:auto; color:var(--warning)">')


# 4. System Architecture Dotted Lines
arch_svg = """<svg style="position:absolute; width:100%; height:100%; top:0; left:0; pointer-events:none; z-index:1;" viewBox="0 0 1000 150" preserveAspectRatio="none">
              <!-- Connector from User to Observability Stack -->
              <!-- Starts at x=80, y=70 (bottom of User node), goes down to y=120, right to x=460, up to y=100 (bottom left of Obs node) -->
              <path d="M 80 90 L 80 130 L 460 130 L 460 115" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 4" />
              <!-- Connector from Approval Workflow to Observability Stack -->
              <!-- Starts at x=920, y=70, goes down to 120, left to 540, up to 100 -->
              <path d="M 920 90 L 920 130 L 540 130 L 540 115" fill="none" stroke="#475569" stroke-width="1.5" stroke-dasharray="4 4" />
              
              <!-- Arrow heads (pointing UP at the end of the paths) -->
              <polygon points="460,115 457,120 463,120" fill="#475569" />
              <polygon points="540,115 537,120 543,120" fill="#475569" />
            </svg>"""

html = re.sub(r'<svg style="position:absolute; width:100%; height:100%; top:0; left:0; pointer-events:none; z-index:1;" viewBox="0 0 1000 150".*?</svg>', arch_svg, html, flags=re.DOTALL)


# 5. Architecture nodes styling
# Make arrows smaller and less bright
html = html.replace('<div class="arch-arrow">→</div>', '<div class="arch-arrow" style="color:#1f2937;">→</div>')
# Make the background of arch nodes slightly different to match the image
html = html.replace('background: var(--bg); border: 1px solid var(--border);', 'background: #0b1120; border: 1px solid #1e293b;')


# 6. Compliance Posture dots
html = html.replace('<div class="comp-item-label"><span class="dot"></span> HIPAA</div>', '<div class="comp-item-label"><span class="dot" style="background-color:var(--success)"></span> HIPAA</div>')
html = html.replace('<div class="comp-item-label"><span class="dot"></span> SOC 2</div>', '<div class="comp-item-label"><span class="dot" style="background-color:var(--success)"></span> SOC 2</div>')
html = html.replace('<div class="comp-item-label"><span class="dot"></span> ISO 27001</div>', '<div class="comp-item-label"><span class="dot" style="background-color:var(--success)"></span> ISO 27001</div>')
html = html.replace('<div class="comp-item-label"><span class="dot"></span> Internal Policies</div>', '<div class="comp-item-label"><span class="dot" style="background-color:var(--success)"></span> Internal Policies</div>')


with open('dashboard.html', 'w') as f:
    f.write(html)

