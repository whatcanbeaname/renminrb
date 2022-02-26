# -*- coding: utf-8 -*-

import os
import shutil
from datetime import datetime
from modules.emails.sendemail import MySendEmail
from modules.periodical_tasks.periodical import start
from modules.requestdata.request_data import request_from
from modules.zippers.zipper import zip_file
from multiprocessing import Pool
from typing import List, Dict

DOWNLOAD_DIR_PATH = './download/'
DOWNLOAD_ZIP_FILE = './download.zip'
CONFIG_FILE_PATH = './config'

class Renminrb:
    def __init__(self, home_page_url, enable_zip=False, sendmail=False):
        self.home_url = home_page_url
        self.config: Dict = {}
        self.enable_zip = enable_zip
        self.enable_mail = sendmail
        self.has_attach = False

    def download(self):
        time0 = datetime.now()
        print('------ 开始下载人民日报评论版文章 ------')
        sel = request_from(self.home_url, apparent_encoding=True) #从主页获取各栏目url和名称
        tag = sel.css('.t03').css('a').getall()
        for t1 in tag:  # <a href="http://opi...html" target="_blank">人民时评</a>
            column = t1.split('>')[1].split('<')[0] #栏目名称
            if column != '':
                column_url = t1.split('>')[0].split('"')[1] #栏目url
                # download articles in category
                print(f'开始下载 【{column}】 板块的评论文章...')
                sel = request_from(column_url, apparent_encoding=True)
                tag = sel.css('.t11 a:link').getall()
                if not tag:
                    tag = sel.css('.t10l14bl').css('a').getall()
                title_list: List[str] = []
                count: int = 2  # 有重名时以数字区分，从2开始标注
                with open('./temp/' + column + '文章列表.txt', mode='a') as f:  # a表示将新内容写到文件末尾
                    for t in tag:
                        article_name = t.split('>')[1].split('<')[0]
                        article_url = 'http://opinion.people.com.cn' + t.split('"')[1]
                        if self.is_new_article(article_url, column): # 是新文章才下载
                            if  article_name != "下一页" and  article_name != "上一页":
                                if  article_name in title_list:
                                    article_name =  article_name + str(count)  # 文章标题有重名时加数字以区别
                                    count += 1
                                title_list.append( article_name)
                                f.write(article_url + '\n')
                                # download one article
                                sel = request_from(article_url, apparent_encoding=True)
                                tag = sel.css('.rm_txt_con p ::text').getall()
                                with open(self.download_path(column) + '/' + article_name + '.txt', mode='w', encoding='utf-8') as ff:
                                    print(f'正在下载: {article_name}')
                                    ff.write(article_name + '\n\n')
                                    for tg in tag:
                                        tg = tg.strip().split('分享让更多人看到')[0]
                                        ff.write(tg + '\n\n')
                if len(title_list) == 0:
                    print(f'【{column}】板块暂无新文章！')
                    print('------------------------------------------------')
                else:
                    print(f'【{column}】板块本次更新文章 {len(title_list)} 篇')
                    print('------------------------------------------------')
        print("文章下载完毕！耗时: ", datetime.now() - time0)

    @staticmethod
    def prepare_work():
        if os.path.exists(DOWNLOAD_DIR_PATH):
            shutil.rmtree(DOWNLOAD_DIR_PATH)  # 删除非空文件夹用shutil库才行
        if os.path.exists(DOWNLOAD_ZIP_FILE):
            os.remove(DOWNLOAD_ZIP_FILE)
        if not os.path.exists('./temp'):
            os.mkdir('./temp')

    @staticmethod
    def download_path(column: str):
        if not os.path.exists(DOWNLOAD_DIR_PATH):
            os.mkdir(DOWNLOAD_DIR_PATH)
        if not os.path.exists(DOWNLOAD_DIR_PATH + column):
            os.mkdir(DOWNLOAD_DIR_PATH + column)
        return DOWNLOAD_DIR_PATH + column

    @staticmethod
    def is_new_article(article_url: str, column: str):
        for url in open('./temp/' + column + '文章列表.txt', mode="r"):
            if article_url == url.strip():
                return False
        return True

    def read_config(self):
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip('\n')  # 使用readlines结尾会有个换行符
                s0, s1 = line.split(':')
                self.config[s0] = s1

    def __call__(self):
        self.prepare_work()
        self.download()
        if self.enable_zip:
            zip_file(DOWNLOAD_DIR_PATH[:-1])
        if self.enable_mail and os.path.exists(DOWNLOAD_ZIP_FILE):
            self.read_config()
            receivers = []
            for s in self.config['receiver'].split(','):
                receivers.append(s)
            if self.config['attach_dir']:
                self.has_attach = True
            MySendEmail(self.config['mail_license'], self.config['sender'], receivers,
                   self.config['subject'], self.config['content'], has_attach=self.has_attach,
                   attach_dir=self.config['attach_dir'], attach_name=self.config['attach_name'])()
        else:
            if self.enable_mail:
                print('mail send enabled, but zip file not found, so skip mail sending!')


def job():
    url = 'http://opinion.people.com.cn/GB/8213/353915/index.html'
    renminrb = Renminrb(url, enable_zip=True, sendmail=True)
    renminrb()

start(job)
# job()
