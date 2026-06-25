import os
import re

files = [
    ('index.html', 'home'),
    ('about.html', 'about'),
    ('members.html', 'members'),
    ('research.html', 'research'),
    ('projects.html', 'projects'),
    ('achievements.html', 'achievements'),
    ('links.html', 'links'),
    ('others.html', 'others')
]

# Read css and js
with open('style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open('main.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Additional JS for SPA routing
spa_js = """
// SPA Navigation Logic
function navigateTo(pageId) {
    document.querySelectorAll('.page-section').forEach(sec => {
        sec.style.display = 'none';
    });
    const target = document.getElementById('page-' + pageId);
    if (target) {
        target.style.display = 'block';
    }
    window.scrollTo(0, 0);
    
    // Close mobile menu if open
    const navLinks = document.querySelector('.nav-links');
    if (navLinks && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        const icon = document.querySelector('.mobile-menu-btn i');
        if (icon) {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            const pageId = href.substring(1); // remove #
            navigateTo(pageId);
            history.pushState(null, '', href);
        });
    });

    // Handle initial load
    const hash = window.location.hash.substring(1) || 'home';
    navigateTo(hash);
    
    // Handle back button
    window.addEventListener('popstate', () => {
        const hash = window.location.hash.substring(1) || 'home';
        navigateTo(hash);
    });
});
"""

js_content += "\n" + spa_js

# Base template
html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="徳島大学 生態系管理工学研究室の公式ウェブサイトです。">
  <title>徳島大学 生態系管理工学研究室 (Ecosystem Management Lab)</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
{css_content}
.page-section {{ display: none; }}
#page-home {{ display: block; }}
  </style>
</head>
<body>

  <header>
    <div class="nav-container">
      <a href="#home" class="logo">
        生態系管理工学研究室
        <span>徳島大学 工学部 建設工学科</span>
      </a>
      <button class="mobile-menu-btn"><i class="fas fa-bars"></i></button>
      <ul class="nav-links">
        <li><a href="#home">ホーム</a></li>
        <li><a href="#about">研究室紹介</a></li>
        <li><a href="#members">メンバー</a></li>
        <li><a href="#research">研究テーマ</a></li>
        <li><a href="#projects">卒業・修士研究</a></li>
        <li><a href="#achievements">研究業績</a></li>
        <li><a href="#links">リンク</a></li>
        <li><a href="#others">その他</a></li>
      </ul>
    </div>
  </header>

  <div id="content-area">
"""

footer_template = f"""  </div>

  <footer>
    <div class="footer-content">
      <div class="footer-logo">徳島大学 生態系管理工学研究室</div>
      <p>〒770-8506 徳島市南常三島町2-1 建設棟3F</p>
      <div class="social-links">
        <a href="https://www.facebook.com/" target="_blank" class="social-icon" aria-label="Facebook">
          <i class="fab fa-facebook-f"></i>
        </a>
      </div>
    </div>
    <div class="copyright">
      &copy; 2026 徳島大学 工学部 建設工学科 生態系管理工学研究室. All Rights Reserved.
    </div>
  </footer>

  <script>
{js_content}
  </script>
</body>
</html>
"""

final_html = html_template

for filename, page_id in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract header and main sections
            # Some pages have <div class="page-header"> before <main>
            header_match = re.search(r'<div class="page-header">.*?</div>', content, re.DOTALL)
            main_match = re.search(r'<main.*?>(.*?)</main>', content, re.DOTALL)
            
            page_html = f'\n    <section id="page-{page_id}" class="page-section">\n'
            
            if header_match:
                page_html += header_match.group(0) + '\n'
            
            if main_match:
                page_html += f'      <main class="container fade-in-section">\n{main_match.group(1)}\n      </main>\n'
            
            page_html += '    </section>\n'
            
            final_html += page_html
    except Exception as e:
        print(f"Error reading {filename}: {e}")

final_html += footer_template

with open('single_page_embed.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Generated single_page_embed.html")
