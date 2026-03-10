# -*- coding: utf-8 -*-
"""
热点新闻海报生成器（HTML版本）
生成可以直接在浏览器中打开的HTML海报
"""

import os


def generate_news_poster_html(
    title,
    subtitle,
    content_lines,
    output_file='news_poster.html',
    scheme='tech'
):
    """
    生成HTML格式的新闻海报

    Args:
        title: 主标题
        subtitle: 副标题
        content_lines: 内容列表
        output_file: 输出HTML文件名
        scheme: 配色方案
    """

    # 配色方案
    colors = {
        'tech': {
            'background': '#1a1a2e',
            'title': '#00d4ff',
            'subtitle': '#7b68ee',
            'content': '#e0e0e0',
            'accent': '#ff6b6b',
            'number': '#ffd700'
        },
        'classic': {
            'background': '#ffffff',
            'title': '#2c3e50',
            'subtitle': '#e74c3c',
            'content': '#34495e',
            'accent': '#3498db',
            'number': '#e74c3c'
        },
        'warm': {
            'background': '#fff8e1',
            'title': '#ff6f00',
            'subtitle': '#ff8f00',
            'content': '#5d4037',
            'accent': '#ffca28',
            'number': '#ff6f00'
        },
        'dark': {
            'background': '#0d1117',
            'title': '#58a6ff',
            'subtitle': '#f78166',
            'content': '#c9d1d9',
            'accent': '#2ea043',
            'number': '#f78166'
        }
    }

    color = colors.get(scheme, colors['tech'])

    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #f0f0f0;
            padding: 20px;
        }}

        .poster {{
            width: 540px;
            height: 960px;
            background: {background};
            padding: 40px 30px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 4px solid {accent};
        }}

        .title {{
            font-size: 36px;
            font-weight: bold;
            color: {title_color};
            line-height: 1.4;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: 20px;
            color: {subtitle_color};
            font-weight: 500;
            line-height: 1.5;
        }}

        .content {{
            flex: 1;
        }}

        .item {{
            display: flex;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid {accent};
            align-items: flex-start;
        }}

        .number {{
            font-size: 48px;
            font-weight: bold;
            color: {number_color};
            min-width: 60px;
            margin-right: 15px;
            line-height: 1.2;
        }}

        .text {{
            flex: 1;
            font-size: 16px;
            color: {content_color};
            line-height: 1.6;
            padding-top: 8px;
        }}

        .footer {{
            text-align: center;
            padding-top: 20px;
            border-top: 4px solid {accent};
        }}

        .footer-text {{
            font-size: 18px;
            color: {subtitle_color};
            font-weight: bold;
        }}

        .btn-download {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: {accent};
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}

        .btn-download:hover {{
            background: {title};
        }}

        .decorative {{
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: {accent};
            opacity: 0.1;
        }}

        .decorative-1 {{
            top: -50px;
            right: -50px;
        }}

        .decorative-2 {{
            bottom: -50px;
            left: -50px;
        }}
    </style>
</head>
<body>
    <button class="btn-download" onclick="downloadPoster()">下载海报</button>
    <button class="btn-download" style="top: 70px;" onclick="window.print()">打印海报</button>

    <div class="poster" id="poster">
        <div class="decorative decorative-1"></div>
        <div class="decorative decorative-2"></div>

        <div class="header">
            <div class="title">{title}</div>
            <div class="subtitle">{subtitle}</div>
        </div>

        <div class="content">
            {content_items}
        </div>

        <div class="footer">
            <div class="footer-text">一生之码 | AI趋势洞察</div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        function downloadPoster() {{
            const poster = document.getElementById('poster');
            html2canvas(poster, {{
                scale: 2,
                useCORS: true,
                backgroundColor: '{background}'
            }}).then(canvas => {{
                const link = document.createElement('a');
                link.download = 'news_poster.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            }});
        }}
    </script>
</body>
</html>"""

    # 生成内容项HTML
    content_items_html = ""
    for i, content in enumerate(content_lines, 1):
        content_items_html += """
            <div class="item">
                <div class="number">%02d</div>
                <div class="text">%s</div>
            </div>
        """ % (i, content)

    # Fill template
    html = html_template.format(
        title=title,
        subtitle=subtitle,
        content_items=content_items_html,
        background=color['background'],
        accent=color['accent'],
        title_color=color['title'],
        subtitle_color=color['subtitle'],
        content_color=color['content'],
        number_color=color['number']
    )

    # Write to file
    import io
    with io.open(output_file, 'w', encoding='utf-8') as f:
        f.write(html.decode('utf-8') if isinstance(html, bytes) else html)

    print("Poster generated: %s" % output_file)
    print("  Open in browser to view and download")
    return output_file


def create_ai_trends_poster():
    """Create 2026 AI trends poster"""
    title = "2026年AI十大趋势曝光"
    subtitle = "这一年被定性为关键转折点，90%的人还没意识到..."

    # Extract key points from the article
    content_lines = [
        "世界模型：AI开始理解真实的物理世界，从感知迈向认知",
        "具身智能：机器人进入工厂、仓库、家庭，实现与物理世界深度交互",
        "多智能体：AI之间有了通用语言，可以互相配合协同解决问题",
        "AI+Science：蛋白质预测、材料设计、气候模拟，科研周期大幅缩短",
        "大模型：从参数竞争转向推理竞争，多模态、高效率、专业化",
        "AI医生：影像诊断准确率超过人类，新药研发周期从5年缩短到1年",
        "无人驾驶：多个城市开放L4级自动驾驶商业运营",
        "人机协作：AI不是替代人类，而是增强人类的能力",
        "企业智能体：AI进入核心业务，研发、客服、运营全面智能化",
        "AI治理：全球加速制定AI治理规则，确保AI安全可控"
    ]

    # 生成多种配色版本
    schemes = ['tech', 'classic', 'warm', 'dark']

    for scheme in schemes:
        output_file = 'ai_trends_poster_%s.html' % scheme
        generate_news_poster_html(
            title=title,
            subtitle=subtitle,
            content_lines=content_lines,
            output_file=output_file,
            scheme=scheme
        )


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    print("Starting news poster generation...\n")
    create_ai_trends_poster()
    print("\nAll posters generated!")
    print("\nUsage tips:")
    print("   1. Open HTML file in browser to view poster")
    print("   2. Click 'Download' button to save as PNG")
    print("   3. Click 'Print' button to print or save as PDF")
