import requests
import proxy.proxypool.storages.redis as redis


PROXY_POOL_URL = 'http://localhost:5555/random'
url = 'https://movie.douban.com/top250?start=%s&filter='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
n=1
conn = None

def get_proxy_by_request():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

def get_proxy_by_redis():
    global conn
    if (conn == None):
        conn = redis.RedisClient()
    result = conn.random().string()
    print(result)
    return result

def request_douban(url):
    try:
        # proxies参数必须是字典类型
        proxies = {
            "http": "http://" + get_proxy_by_redis()
        }

        # status_code=418 被反爬虫拦截，需要添加请求头
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

if __name__ == '__main__':
    for page in range(0, 10):
        html = request_douban(url % (str(page * 25)))
        print(html)