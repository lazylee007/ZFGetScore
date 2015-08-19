# -*- coding:gb2312 -*-
import urllib, urllib2, cookielib
import re, os, string
from bs4 import BeautifulSoup
# from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

baseUrl = 'http://222.24.19.201/'
codeUrl = 'CheckCode.aspx'
loginUrl = 'default2.aspx'
scoreUrl = 'xscjcx.aspx'

def downImg(url, name):
    '''
    ������֤��
    :param url:��֤���ȡ�ӿ�
    :param name: ��֤��洢�ļ���
    :return:
    '''
    try:
        req = urllib2.Request(url)
        req = urllib2.urlopen(req)
        content = req.read()

        file = open(os.getcwd() + '/' + name, 'w+b')
        file.write(content)
        file.close()
    except Exception, e:
        print 'Error :', e

def setCookie():
    '''
    ����cookie
    :return:cookie���
    '''
    cookie = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    opener.open(baseUrl)
    return cookie

def login(username, password, cookie):
    '''
    ��¼����ϵͳ
    :param username:�û���
    :param password:����
    :param cookie:setcookie��cookie���
    :return:�û����Լ�session_id
    '''
    request = urllib2.Request(baseUrl)
    text = urllib2.urlopen(request).read()
    downImg(baseUrl + codeUrl, 'code.png')
    # image = Image.open('code.png')
    # print image_to_string(image)
    code = raw_input('��������֤��:')
    soup = BeautifulSoup(text, 'html.parser')
    _VIEWSTATE = soup.find_all('input')[0].get('value')
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
        'Referer'    : baseUrl
    }
    postData = {
        '__VIEWSTATE' : _VIEWSTATE,
        'txtUserName' : username,
        'TextBox2' : password,
        'txtSecretCode' : code,
        'RadioButtonList1' : 'ѧ��',
        'Button1' : '',
        'lbLanguage' : '',
        'hidPdrs' : '',
        'hidsc' : '',
    }
    postData = urllib.urlencode(postData)
    request = urllib2.Request(baseUrl + loginUrl, postData, headers)
    response = urllib2.urlopen(request)
    text = response.read()
    soup = BeautifulSoup(text, 'html.parser')
    if re.search('��֤�벻��ȷ', text):
        print '��֤�����'
        exit(1)
    elif re.search('<span id="xhxm">', text):
        result = {}
        name = soup.find(id = 'xhxm').string
        name = name.decode('gb2312').encode('gb2312')
        name = string.replace(name, 'ͬѧ', '')
        result['name'] = name
        session_id = cookie._cookies['222.24.19.201']['/']['ASP.NET_SessionId'].value
        result['session_id'] = session_id
        return result
    else:
        print '��¼ʧ��'
        exit(1)
def getScore(username, name, session_id, ddlXN, ddlXQ):
    '''
    ��ȡ�ɼ�
    :param username:�û���
    :param name:�û�����
    :param session_id:session_id
    :param ddlXN:ѧ��
    :param ddlXQ:ѧ��
    :return:����ɼ�
    '''
    if ddlXQ == 0:
        btn_xq = 'ѧ��ɼ�'
    else:
        btn_xq = 'ѧ�ڳɼ�'
    url = baseUrl + scoreUrl + '?xh=' + str(username) + '&xm=' + str(name) + '&gnmkdm=N121605'
    headers = {
        'Referer' : baseUrl + '/xs_main.aspx?xh=' + username,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
        'Cookie' : 'ASP.NET_SessionId=' + session_id
    }

    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    text = response.read()
    soup = BeautifulSoup(text, 'html.parser')
    department = soup.find(id = 'lbl_xy').string.decode('gb2312').encode('gb2312')
    department = string.replace(department, 'ѧԺ��', '')
    major = soup.find(id = 'lbl_zymc').string.decode('gb2312').encode('gb2312')
    classes = soup.find(id = 'lbl_xzb').string.decode('gb2312').encode('gb2312')
    classes = string.replace(classes, '�����ࣺ', '')
    _VIEWSTATE = soup.find_all('input')[2].get('value')
    print department
    print major
    print classes
    headers = {
        'Referer'    : url,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
        'Cookie' : 'ASP.NET_SessionId=' + session_id
    }

    postData = {
        '__EVENTTARGET' : '',
        '__EVENTARGUMENT' : '',
        '__VIEWSTATE' : _VIEWSTATE,
        'hidLanguage' : '',
        'ddlXN' : ddlXN,
        'ddlXQ' : ddlXQ,
        'ddl_kcxz' :'',
        'btn_xq' : btn_xq,
    }
    postData = urllib.urlencode(postData)
    request = urllib2.Request(url, postData, headers)
    response = urllib2.urlopen(request)
    text = response.read()
    soup = BeautifulSoup(text, 'html.parser')
    datagrid = soup.find(id = 'Datagrid1')
    trs = datagrid.find_all('tr')
    length =  trs.__len__()
    for i in range(1, length):
        tds = trs[i].find_all('td')
        print '�γ�����%s �ɼ���%s' % (tds[3].string, tds[8].string)


if __name__ == '__main__':
    cookie = setCookie()
    username = raw_input('����������û�����')
    password = raw_input('������������룺')
    result = login(username, password, cookie)
    name = result['name']
    print name
    session_id = result['session_id']
    ddlXN = raw_input('������ѧ�꣺')
    # btn_xq = raw_input('��ѡ���ѯ��ʽ:\n1����ѧ���ѯ\n2����ѧ�ڲ�ѯ\n�������ֽ���ѡ��')
    # print btn_xq
    btn_xq = '2'
    if btn_xq == '2':
        ddlXQ = raw_input('������ѧ�ڣ�')
    else:
        ddlXQ = 0
    getScore(username, name, session_id, ddlXN, ddlXQ)