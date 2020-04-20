from flask import Flask, request
from flask_caching import Cache
import requests
import os

app = Flask(__name__)
cache = Cache()
cache.init_app(app=app, config={'CACHE_TYPE' : 'simple'})
protocol = os.getenv('CDN_PROTOCOL') or 'https'
domain = os.getenv('CDN_HOST') or 'qnapclub.eu'

@app.errorhandler(500)
def internal_error(error):
    return '代理服务异常, exception: ' + error.original_exception.args[0]

@app.route('/')
def index():
    return '欢迎使用Fansy\'s QnapClub代理'

@app.route('/cache/repo.xml', methods=["GET", "POST"])
@cache.cached(timeout=7200, key_prefix='repo')
def cache_repo():
    content = repo()
    return content

@app.route('/cache/clear', methods=["GET"])
def cache_clear():
    cache.delete('repo')
    return 'clear cache success.'
    
@app.route('/repo.xml', methods=["GET", "POST"])
def repo():
    url = 'https://qnapclub.eu/en/repo.xml'
    headers = {h[0]: h[1] for h in request.headers}
    headers['Host'] = 'qnapclub.eu'
    response = requests.request(request.method, url, headers=headers)
    return parse_content(response.content)

def parse_content(content):
    content = str(content, encoding='utf-8')
    content = content.replace("https://qnapclub.eu/en/qpkg/model/download", get_cdn_url('/en/qpkg/model/download'))
    content = content.replace("https://cdn.qnapclub.eu", get_cdn_url(''))
    return content
    
def get_cdn_url(url):
    return protocol + '://' + domain + url

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)