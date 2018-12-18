# !/usr/bin/env python3
# -*- coding : utf-8 -*-
import requests
import re


class Login:
    def __init__(self):
        self.get_ipv6_url = 'http://cippv6.ustb.edu.cn/get_ip.php'
        self.login_url = 'http://202.204.48.66/'
        self.login_result_url = 'http://202.204.48.66/1.htm'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) ' +
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/64.0.3282.186 Safari/537.36'
        }

    def __get_ipv6_address(self):
        ipv6_html = requests.get(self.get_ipv6_url).text
        ipv6_address = ipv6_html[13:].split("'")[0]
        return ipv6_address

    def __get_info(self):
        login_success_html = requests.get(url=self.login_result_url, headers=self.headers).text
        uid = re.findall('uid=\'\d{8}\'', login_success_html)[0][5:-1]
        fee = int(re.findall('fee=\'\d+', login_success_html)[0][5:])/10000
        print('账号：', uid)
        print('余额：', fee, '元')

    def login(self, stuid, pwd):
        ipv6_addr = self.__get_ipv6_address()
        data = {
            'DDDDD': stuid,
            'upass': pwd,
            'v6ip': ipv6_addr,
            '0MKKey': '123456789'
        }
        response = requests.post(url=self.login_url, data=data, headers=self.headers)
        suc = re.search('您已经成功登录', response.text)
        # Msg = re.findall('Msg=\d\d', response.text)
        if suc:
            print('登录成功！')
            self.__get_info()
        else:
            print('登录失败！用户名密码错误或费用超支！')


if __name__ == '__main__':
        student_number = ''     # 用户名（学号）
        password = ''           # 密码
        try:
            new_login = Login()
            new_login.login(student_number, password)
        except Exception as e:
            print("发生异常！\n信息：", e)
