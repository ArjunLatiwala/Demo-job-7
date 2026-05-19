import re

with open('dashboard.html', 'r') as f:
    html = f.read()

# 1. Fix KPI Icons
blue_icon = '<svg viewBox="0 0 24 24" width="10" height="10"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>'
html = re.sub(r'<div class="kpi-icon blue"><svg.*?</svg></div>', f'<div class="kpi-icon blue">{blue_icon}</div>', html, count=1, flags=re.DOTALL)

purple_icon = '<svg viewBox="0 0 24 24" width="10" height="10"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
html = re.sub(r'<div class="kpi-icon purple"><svg.*?</svg></div>', f'<div class="kpi-icon purple">{purple_icon}</div>', html, count=1, flags=re.DOTALL)

amber_icon = '<svg viewBox="0 0 24 24" width="10" height="10"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="17" y1="11" x2="23" y2="11"></line></svg>'
html = re.sub(r'<div class="kpi-icon amber"><svg.*?</svg></div>', f'<div class="kpi-icon amber">{amber_icon}</div>', html, count=1, flags=re.DOTALL)

green_icon = '<svg viewBox="0 0 24 24" width="10" height="10"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
html = re.sub(r'<div class="kpi-icon green"><svg.*?</svg></div>', f'<div class="kpi-icon green">{green_icon}</div>', html, count=1, flags=re.DOTALL)

yellow_icon = '<svg viewBox="0 0 24 24" width="10" height="10"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>'
html = re.sub(r'<div class="kpi-icon yellow"><svg.*?</svg></div>', f'<div class="kpi-icon yellow">{yellow_icon}</div>', html, count=1, flags=re.DOTALL)


# 2. Fix KPI Sparklines (Exact matching curves to the image)
# Blue: starts low, rises to peak, drops, rises to small peak
blue_chart = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 16 Q 10 16, 20 13 T 40 16 T 60 13 T 80 16 T 100 12" fill="none" stroke="#3b82f6" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-chart">\s*<svg viewBox="0 0 100 20".*?</svg>\s*</div>', f'<div class="kpi-chart">\n            {blue_chart}\n          </div>', html, count=1, flags=re.DOTALL)

# Purple: gently rippling
purple_chart = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 17 Q 20 17, 30 14 T 50 17 T 70 14 T 90 17 L 100 16" fill="none" stroke="#8b5cf6" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-chart">\s*<svg viewBox="0 0 100 20".*?</svg>\s*</div>', f'<div class="kpi-chart">\n            {purple_chart}\n          </div>', html, count=1, flags=re.DOTALL)

# Amber: flat then small rise then flat then big rise then drops
amber_chart = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 18 L 30 18 Q 40 18, 50 16 T 70 18 Q 80 18, 90 12 T 100 16" fill="none" stroke="#f59e0b" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-chart">\s*<svg viewBox="0 0 100 20".*?</svg>\s*</div>', f'<div class="kpi-chart">\n            {amber_chart}\n          </div>', html, count=1, flags=re.DOTALL)

# Green: very slight wave, mostly flat
green_chart = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 17 Q 25 17, 40 15 T 70 17 T 90 15 L 100 16" fill="none" stroke="#10b981" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-chart">\s*<svg viewBox="0 0 100 20".*?</svg>\s*</div>', f'<div class="kpi-chart">\n            {green_chart}\n          </div>', html, count=1, flags=re.DOTALL)

# Yellow: flat, slight drop, long flat, huge rise, huge drop, flat
yellow_chart = '<svg viewBox="0 0 100 20" preserveAspectRatio="none" style="width:100%;height:100%;"><path d="M0 15 L 40 15 Q 50 15, 60 18 T 80 15 Q 90 5, 95 10 T 100 15" fill="none" stroke="#facc15" stroke-width="1.5"/></svg>'
html = re.sub(r'<div class="kpi-chart">\s*<svg viewBox="0 0 100 20".*?</svg>\s*</div>', f'<div class="kpi-chart">\n            {yellow_chart}\n          </div>', html, count=1, flags=re.DOTALL)


# 3. Fix Compliance Donut shadow and styling
# Adding drop-shadow to the green arc and tweaking the arc lengths and text color
new_comp_chart = '''<svg viewBox="0 0 200 120" style="width: 100px; height: 60px;">
                <defs>
                  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="0.3"/>
                  </filter>
                </defs>
                <!-- Background track -->
                <path d="M 15,100 A 85,85 0 0,1 185,100" fill="none" stroke="#1f2937" stroke-width="24" stroke-linecap="round"/>
                <!-- Progress -->
                <path d="M 15,100 A 85,85 0 0,1 182,85" fill="none" stroke="#10b981" stroke-width="24" stroke-linecap="round" filter="url(#shadow)"/>
              </svg>'''

html = re.sub(r'<svg viewBox="0 0 200 120".*?</svg>', new_comp_chart, html, flags=re.DOTALL)

# Fix Compliance Text colors
html = html.replace('<div class="comp-item-val">Compliant</div>', '<div class="comp-item-val" style="color: #059669;">Compliant</div>')


with open('dashboard.html', 'w') as f:
    f.write(html)
