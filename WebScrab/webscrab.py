# -*- coding: utf-8 -*-

from urllib import request
import chardet
from os import path, makedirs, getcwd
import copy
from html import parser
from shutil import rmtree

root_url = u"http://www.opencv.org.cn/opencvdoc/2.3.2/html/index.html"


def get_base_url_path(root_url):
    result = request.urlparse(root_url)
    return request.urlunparse((result.scheme, result.netloc, path.dirname(result.path),
                               '', '', ''))


local_dir = './TempPages/opencvdoc/webs'
new_urls = set()
all_reqeusted_urls = set()

all_img_srcs = set()


def gen_new_url(base_url, value):
    # get base url path
    base_url_parse_result = request.urlparse(base_url)
    base_url_path = base_url_parse_result.path

    new_url_rel_path = path.join(base_url_path,value).replace('\\','/')

    new_path_splits = []

    new_url_path = ''
    # get real path
    last_i = ''

    #print(new_url_rel_path.split('/')[1:])
    for i in new_url_rel_path.split('/')[1:]:
        if i != '..':
            new_path_splits.append(i)
        else:
            new_path_splits.remove(new_path_splits[-1])

    for i in new_path_splits:
        new_url_path = new_url_path + '/' + i

    return request.urlunparse(
        (base_url_parse_result.scheme,
         base_url_parse_result.netloc, new_url_path,
         '', '', ''))


class MyParser(parser.HTMLParser):
    def __init__(self, base_url):
        super(MyParser, self).__init__()
        self.urls = set()
        self.imgs = set()
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):

        # 这里重新定义了处理开始标签的函数
        if tag == 'a':
            # 判断标签<a>的属性
            for name, value in attrs:
                if name == 'href':
                    if "http://" in value or "https://" in value:
                        # do not  parse external site html,
                        # internal site html use relative url
                        continue

                    if ".html#" in value or "#" in value:
                        #  in case the url is a part of an html, like
                        """ <a class="reference internal" 
                        href="core/table_of_content_core/table_of_content_core.html
                        #table-of-content-core"><em>core 模块. 核心功能</em></a>"""

                        continue

                    new_url = gen_new_url(self.base_url,value)
                    self.urls.add(new_url)

        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    if "http://" in value or "https://" in value:
                        # do not  parse external site img,
                        # internal site html use relative url
                        continue
                    new_img = gen_new_url(self.base_url,value)
                    self.imgs.add(new_img)


def UrlParse(url, base_url, root_path):
    """"
    parsing ref_url,generate local saving dir and target file name
    for example:
        Input ref_url: http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/tutorials
        /tutorials.html"
        Output saving_path: [root_path]/doc/tutorials  ref_html:tutorials.html

    outputs will be used to create local file to save the ref_url contents

    it can also be used in img element parsing
    """
    ref_dir = url.split(base_url)[1].split(r'/')
    saving_path = copy.deepcopy(root_path)
    print("ref split rel dir:{}".format(ref_dir))

    for item in ref_dir[1:-1]:
        saving_path = path.join(saving_path, item)

    ref_html = ref_dir[-1]
    return saving_path, ref_html


def parseAndDownloadWebPage(url, local_root_dir):
    base_url = get_base_url_path(url)
    saving_path, url_html = UrlParse(url, base_url, local_root_dir)

    if not path.exists(saving_path):
        print("makedirs {}".format(saving_path))
        makedirs(saving_path)

    web_file = path.join(saving_path, url_html)

    if path.exists(web_file):
        print("Error: web file already exist, while the relative url is not requested")
        return set(), set()

    try:
        webpage = request.urlopen(url).read()
    except:
        print("visit error url:{}".format(url))
        return set(), set()

    print("success visit url:{}".format(url))
    charset = chardet.detect(webpage)

    # print(charset)

    with open(web_file, 'w', encoding=charset['encoding']) as f:
        for line in webpage.decode(charset['encoding']):
            f.write(line)

    # parsing web contents, selecting site urls and images
    hmparser = MyParser(base_url)
    hmparser.feed(webpage.decode(charset['encoding']))
    print(hmparser.urls)
    print(hmparser.imgs)

    return hmparser.urls, hmparser.imgs


def downloadImage(img_src, local_root_dir):
    saving_path, img = UrlParse(img_src, local_root_dir)

    if not path.exists(saving_path):
        makedirs(saving_path)

    img_file = path.join(saving_path, img)

    if path.exists(img_file):
        print("Error: web file already exist, while the relative url is not requested")
        return

    request.urlretrieve(img_src, img_file)


if __name__ == '__main__':

    # scrap index html
    new_urls.add(root_url)

    if path.exists(local_dir):
        rmtree(local_dir)
    else:
        makedirs(local_dir)

    while (1):
        urls = set()
        imgs = set()

        if new_urls == set():
            break

        for url in new_urls:
            all_reqeusted_urls.add(url)
            temp_urls, temp_imgs = parseAndDownloadWebPage(url, local_dir)

            urls = urls | temp_urls
            imgs = imgs | temp_imgs

        # get new urls from already parsed html (remove already requested urls)
        new_urls = urls - (urls & all_reqeusted_urls)
        all_img_srcs = all_img_srcs | imgs

    for img_src in all_img_srcs:
        downloadImage(img_src, local_dir)
