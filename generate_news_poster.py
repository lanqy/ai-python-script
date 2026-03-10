# -*- coding: utf-8 -*-
"""
热点新闻海报生成器
支持自定义文字内容、配色方案和布局样式
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
from typing import Tuple, List
import os


class NewsPosterGenerator:
    def __init__(self):
        # 预设配色方案
        self.color_schemes = {
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

    def generate_poster(self, title, subtitle, content_lines, output_path='news_poster.png',
                       width=1080, height=1920, scheme='tech'):
        """
        生成热点新闻海报

        Args:
            title: 主标题
            subtitle: 副标题
            content_lines: 内容列表（每行一个要点）
            output_path: 输出文件路径
            width: 海报宽度（像素）
            height: 海报高度（像素）
            scheme: 配色方案名称
        """
        colors = self.color_schemes.get(scheme, self.color_schemes['tech'])

        # 创建画布
        img = Image.new('RGB', (width, height), colors['background'])
        draw = ImageDraw.Draw(img)

        # 尝试加载中文字体
        title_font = self._get_font(size=80, bold=True)
        subtitle_font = self._get_font(size=50)
        content_font = self._get_font(size=42)
        number_font = self._get_font(size=120, bold=True)

        if not title_font:
            print("警告: 未找到合适的中文字体，使用默认字体（可能无法正确显示中文）")
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            number_font = ImageFont.load_default()

        # 计算各区域高度
        header_height = 400
        content_start = header_height + 50
        line_height = 90

        # 绘制顶部装饰线
        draw.rectangle([0, header_height - 5, width, header_height], fill=colors['accent'])

        # 绘制标题
        title_y = 100
        title_lines = self._wrap_text(draw, title, title_font, width - 100)
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, title_y), line, font=title_font, fill=colors['title'])
            title_y += title_font.size * 1.2

        # 绘制副标题
        if subtitle:
            subtitle_lines = self._wrap_text(draw, subtitle, subtitle_font, width - 120)
            subtitle_y = title_y + 30
            for line in subtitle_lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, subtitle_y), line, font=subtitle_font, fill=colors['subtitle'])
                subtitle_y += subtitle_font.size * 1.1

        # 绘制内容
        y = content_start
        for i, content in enumerate(content_lines, 1):
            # 绘制序号
            number_text = "%02d" % i
            draw.text((80, y), number_text, font=number_font, fill=colors['number'])

            # 绘制内容
            content_x = 200
            content_lines_wrapped = self._wrap_text(draw, content, content_font, width - 250)
            for line in content_lines_wrapped:
                draw.text((content_x, y), line, font=content_font, fill=colors['content'])
                y += line_height

            # 绘制分割线
            y -= line_height // 2
            draw.line([80, y + 10, width - 80, y + 10], fill=colors['accent'], width=2)
            y += 50

        # 绘制底部装饰
        footer_y = height - 150
        draw.rectangle([0, footer_y, width, footer_y + 5], fill=colors['accent'])

        # 绘制底部文字
        footer_text = "一生之码 | AI趋势洞察"
        bbox = draw.textbbox((0, 0), footer_text, font=subtitle_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, footer_y + 30), footer_text, font=subtitle_font, fill=colors['subtitle'])

        # 保存图片
        img.save(output_path, 'PNG', quality=95)
        print("✓ 海报已生成: %s" % output_path)
        return output_path

    def _wrap_text(self, draw, text, font, max_width):
        """将文本换行以适应指定宽度"""
        lines = []
        current_line = ""

        for char in text:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        return lines

    def _get_font(self, size, bold=False):
        """获取字体，优先使用中文字体"""
        # 常见的中文字体路径
        font_paths = [
            # Windows
            r"C:\Windows\Fonts\msyh.ttc",  # 微软雅黑
            r"C:\Windows\Fonts\simhei.ttf",  # 黑体
            r"C:\Windows\Fonts\simsun.ttc",  # 宋体
            r"C:\Windows\Fonts\simkai.ttf",  # 楷体
            # macOS
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            # Linux
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        ]

        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue

        return None


def create_ai_trends_poster():
    """创建2026年AI发展趋势海报"""
    generator = NewsPosterGenerator()

    title = "2026年AI十大趋势曝光"
    subtitle = "这一年被定性为关键转折点，90%的人还没意识到..."

    # 提取文章中的关键点
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
        output_path = 'ai_trends_poster_%s.png' % scheme
        generator.generate_poster(
            title=title,
            subtitle=subtitle,
            content_lines=content_lines,
            output_path=output_path,
            scheme=scheme
        )


if __name__ == '__main__':
    print("🎨 开始生成热点新闻海报...\n")
    create_ai_trends_poster()
    print("\n✅ 所有海报生成完成！")
