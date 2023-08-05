import re
import mistune


def markdown_renderer():
    class CustomRenderer(mistune.HTMLRenderer):
        def paragraph(self, text):
            # 添加高亮背景
            pattern = r'\[highlight\](.*?)\[/highlight\]'
            replacement = r'<span class="highlight">\1</span>'
            text = re.sub(pattern, replacement, text)
            # 添加背景线
            pattern = r'\[bgline\](.*?)\[/bgline\]'
            replacement = r'<span class="bgline">\1</span>'
            text = re.sub(pattern, replacement, text)
            # 添加下划背景线
            pattern = r'\[underline\](.*?)\[/underline\]'
            replacement = r'<span class="underline">\1</span>'
            text = re.sub(pattern, replacement, text)
            # 添加文字居中
            pattern = r'\[underline\](.*?)\[/underline\]'
            replacement = r'<span class="underline">\1</span>'
            text = re.sub(pattern, replacement, text)
            # 添加success框
            pattern = r'\[success\](.*?)\[/success\]'
            replacement = r'<article class="message is-success"><div class="message-body"><p>\1</p></div></article>'
            text = re.sub(pattern, replacement, text)
            # 添加info框
            pattern = r'\[info\](.*?)\[/info\]'
            replacement = r'<article class="message is-info"><div class="message-body"><p>\1</p></div></article>'
            text = re.sub(pattern, replacement, text)
            # 添加warning框
            pattern = r'\[warning\](.*?)\[/warning\]'
            replacement = r'<article class="message is-warning"><div class="message-body"><p>\1</p></div></article>'
            text = re.sub(pattern, replacement, text)
            # 添加自定义文字颜色与文字大小
            pattern = r'\[font\s+color=(.*?)\s*(?:size=(.*?))?\](.*?)\[/font\]'
            replacement = r'<font color="\1" size="\2">\3</font>'
            replaced_text = re.sub(pattern, replacement, text)

            return super().paragraph(replaced_text)

        # 将文章中的图片支持点击放大
        def image(self, alt, url, title=None):
            if title:
                title = 'title="{}"'.format(title)
            else:
                title = ""

            return '<img src="{}" alt="{}" {} class="alignnone">'.format(url, alt, title)

    markdown_text = '''
    ![image](path/to/image.png)

    **[font color=#fff]qwq[/font]**

    > [highlight]test[/highlight]
    '''
    renderer = CustomRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    html = markdown(markdown_text)
    encoded_html = html.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return encoded_html
