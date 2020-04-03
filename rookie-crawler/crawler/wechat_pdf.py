#-*- coding:UTF-8 -*-
import json
import time
import pdfkit
import wechatsogou

import requests

base_url = 'https://mp.weixin.qq.com/mp/profile_ext'
ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)


# 这些信息不能抄我的，要用你自己的才有效
headers = {
    'Connection': 'keep - alive',
    'Accept': '* / *',
    # 自己的
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; 16 X Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1178 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/5947 MicroMessenger/7.0.10.1580(0x27000AFE) Process/toolsmp NetType/WIFI Language/zh_CN ABI/arm64',
    # 自己的
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU2ODYzNTkwMg==&subscene=0&devicetype=android-27&version=27000afe&lang=zh_CN&nettype=WIFI&a8scene=59&session_us=gh_10d1e024f589&pass_ticket=5hro1g3LtVZfBCbJvflTiCeCS4t12DYgWHTcXvU3LbFxRP%2FTNcKK6lb7u%2BB6PrDw&wx_header=1',
    'Accept-Encoding': 'br, gzip, deflate'
}

cookies = {
    'devicetype': 'iOS12.2',
    'lang': 'zh_CN',
    # 自己的
    'pass_ticket': '5hro1g3LtVZfBCbJvflTiCeCS4t12DYgWHTcXvU3LbFxRP/TNcKK6lb7u+B6PrDw',
    'version': '1700042b',
    # 自己的
    'wap_sid2': 'COmfqZQEElxqdzlmOFN5Q0ZpRmloRUwzekJvY1RlUUpXM3dNNnlSbWwzRUNORTRtVGJLczg4Z254VVB1ZFNnTWVUTUhxNlJEYi1QSlEyeGN4b0JXZ2cyaDNtVGhUaDRFQUFBfjCb6Ir0BTgNQJVO',
    'wxuin': '3340537333'
}



def get_params(offset):
    params = {
        'action': 'getmsg',
        # 自己的
        '__biz': 'MzU2ODYzNTkwMg==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        # 自己的
        'pass_ticket': '5hro1g3LtVZfBCbJvflTiCeCS4t12DYgWHTcXvU3LbFxRP/TNcKK6lb7u+B6PrDw',
        # 自己的
        'appmsg_token': '1054_pcZaUhU4XZSzZ9abC1cjOT1ZEnwDWjuIwnW7WQ~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_list_data(offset):
    res = requests.get(base_url, headers=headers, params=get_params(offset), cookies=cookies)
    data = json.loads(res.text)
    can_msg_continue = data['can_msg_continue']
    next_offset = data['next_offset']

    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']

    for data in list_data:
        try:
            if data['app_msg_ext_info']['copyright_stat'] == 11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                # 解决生成的pdf没有图片的问题，先请求内容然后将content_html构造成完整的html，使用pdfkit.from_string()生成pdf
                # try:
                #     content_info = ws_api.get_article_content(content_url)
                # except:
                #     return False
                # html = f'''
                #     <!DOCTYPE html>
                #     <html lang="en">
                #     <head>
                #         <meta charset="UTF-8">
                #         <title>{title}</title>
                #     </head>
                #     <body>
                #     <h2 style="text-align: center;font-weight: 400;">{title}</h2>
                #     {content_info['content_html']}
                #     </body>
                #     </html>
                #     '''
                # pdfkit.from_string(html, './wechat_article/'+title+'.pdf')

                # 自己定义存储路径
                pdfkit.from_url(content_url, './wechat_article/'+title+'.pdf')
                print('获取到原创文章：%s ： %s' % (title, content_url))
        except:
            print('不是图文')

    if can_msg_continue == 1:
        time.sleep(1)
        get_list_data(next_offset)


if __name__ == '__main__':
    get_list_data(0)