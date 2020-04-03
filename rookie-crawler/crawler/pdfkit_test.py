import pdfkit
# pdfkit是基于wkhtmltopdf的python封装，支持URL，本地文件，文本内容到PDF的转换，所以使用pdfkit需要下载wkhtmltopdf

content_url = "https://mp.weixin.qq.com/s?__biz=MzU2ODYzNTkwMg==&amp;mid=2247486609&amp;idx=1&amp;sn=30b06fe5c1900c0ce5a1e075ae6efcb9&amp;chksm=fc8bb400cbfc3d1629ee2d7b1a7738faf639e6fd0adbe2b661823709398a023e7f6915bbd4e9&amp;scene=27#wechat_redirect"
pdfkit.from_url(content_url, 'test.pdf')