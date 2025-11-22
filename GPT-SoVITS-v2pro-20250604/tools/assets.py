js = """
function deleteTheme() {

const params = new URLSearchParams(window.location.search);
if (params.has('__theme')) {
    params.delete('__theme');
    const newUrl = `${window.location.pathname}?${params.toString()}`;
    window.location.replace(newUrl);
}

}
"""

css = """
/* CSSStyleRule */
.markdown {
    padding: 6px 10px;
}

@media (prefers-color-scheme: light) {
    .markdown {
        background-color: lightblue;
        color: #000;
    }
}

@media (prefers-color-scheme: dark) {
    .markdown {
        background-color: #4b4b4b;
        color: rgb(244, 244, 245);
    }
}

::selection {
    background: #ffc078 !important;
}

footer {
    height: 50px !important;           /* 设置页脚高度 */
    background-color: transparent !important; /* 背景透明 */
    display: flex;
    justify-content: center;           /* 居中对齐 */
    align-items: center;               /* 垂直居中 */
}

footer * {
    display: none !important;          /* 隐藏所有子元素 */
}

"""

top_html = """
<div align="center">
    <div style="margin-bottom: 5px; font-size: 15px;">{}</div>
</div>
"""

# 原始 top_html 已備份至 assets.py.backup
# 包含 GitHub、文檔、在線體驗等鏈接的完整版本
