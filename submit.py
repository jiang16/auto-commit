#!/usr/bin/env python  
#-*-coding:utf-8-*-  
      
import sys, os, shutil
import  urllib, urllib2  
import cookielib  
import getpass  
from bs4 import BeautifulSoup  
 
#处理编码问题
reload(sys)
sys.setdefaultencoding("utf-8")

home_url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home'  
login_url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Login/login'      
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}       
 
def Login():    
    cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())  
    opener = urllib2.build_opener(cookie_support)  
    urllib2.install_opener(opener)   
    home_temp = urllib2.urlopen(home_url)  
    uername = raw_input('请输入用户名:')  
    key = getpass.getpass('请输入登录密码:')     
    values = {'user_name': uername, 'password': key}   
    post = urllib.urlencode(values)  
    request = urllib2.Request(login_url, post, headers)  
    response = urllib2.urlopen(request)      
    soup = BeautifulSoup(response.read()) 
    if soup.find(text = 'Logout') != None:  
        print '登录成功：)'
    else:  
        print '登录失败：('
        sys.exit(0)

def Logout():
    urllib2.urlopen('http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Login/logout')
    print '退出登录'

def Contest(cid, do):
    url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Contest/problemlist/cid/' + cid
    soup = BeautifulSoup(urllib2.urlopen(url))
    problem = soup.find_all('tr')
    for tr in problem:
        try:
            td = tr.find_all('td')
            pid = td[0].a['href'][-4:]
            if do == True:
                DownloadCode(cid, pid)
            else:
                Submit(cid, pid)
                print td[0].text + '提交成功'
        except:
            pass

def DownloadCode(cid, pid):
    url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Solution/status/pid/' + pid + '/result/1.html'
    sub = BeautifulSoup(urllib2.urlopen(url))  
    table = sub.find_all('tr')  
    for tr in table:  
        try:  
            td = tr.find_all('td')  
            if td[3].text == 'Accepted' and td[2].a['href'][-9:-5] == pid and (td[6].text == 'g++' or td[6].text == 'gcc'):  
                code_url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Viewcode/view/sid/' + td[0].text   
                code = BeautifulSoup(urllib2.urlopen(code_url)).find(class_ = 'brush:cpp;').text
                with open('/home/lenovo/Code/' + pid + '.cpp', 'w') as f:
                    f.write(code)
                return
        except:  
            pass  

def Submit(cid, pid):
    url = 'http://acm.sdut.edu.cn/onlinejudge2/index.php/Home/Contest/contestsubmit/cid/' + cid + '/pid/' + pid + '.html'
    with open('/home/lenovo/Code/' + pid + '.cpp', 'r') as f:
        code = f.read()
        value = {'cid': cid, 'pid': pid, 'lang': 'g++', 'code': code}
        request = urllib2.Request(url, urllib.urlencode(value), headers) 
        response = urllib2.urlopen(request)
    
if __name__ == '__main__':
    os.mkdir('/home/lenovo/Code')
    Login()
    cid = raw_input('请输入比赛的id:')
    Contest(cid, True)
    Logout()
    Login()
    Contest(cid, False)
    shutil.rmtree('/home/lenovo/Code')
