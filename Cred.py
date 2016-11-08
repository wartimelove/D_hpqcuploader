__author__ = 'kliux'

import urllib
import urllib2
import base64
import re

class ReturnData:
    def __init__(self, code, data):
        self.code = code
        self.data = data

class Session:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password =password
        self.cookies = {}
        self.token = None
        self.retrieve_token()
        self.open_session()

    def __del__(self):
        self.close_session()
        self.discard_token()

    def retrieve_token(self):
        try:
            url = r'%s/qcbin/authentication-point/authenticate' % self.host
            credential = "Basic %s" % base64.b64encode(r'%s:%s' % (self.username,self.password))
            authorization = {r'Authorization':credential,}
            req = urllib2.Request(url,data=None,headers=authorization)
            response = urllib2.urlopen(req)
            cookies = response.headers[r'set-cookie']
            pat = re.compile(r'^LWSSO_COOKIE_KEY=(?P<token>[^;]+);\S+$')
            m = pat.match(cookies)
            if m:
                token = m.group('token')
                self.token = token
                return ReturnData(response.code,token)
            return ReturnData(-1, 'Please Check the format')
        except IOError, ex:
            return ReturnData(-1, ex.message)

    def open_session(self):
        ret = None
        if not self.token:
            ret = self.retrieve_token()

        if ret and not self.token:
            return ret

        try:
            url = r'%s/qcbin/rest/site-session' % self.host
            cookie_key = "LWSSO_COOKIE_KEY=%s" % self.token
            data = urllib.urlencode(r'')
            request_headers = {r'Cookie':cookie_key,}
            request_headers['Content-Type'] = "application/x-www-form-urlencoded"
            req = urllib2.Request(url,data=None,headers=request_headers)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(req,data)
            pat = re.compile(r'^Set-Cookie:\s*(?P<name>[^=]+)=(?P<value>[^;]+);[\w\W]*$')
            cookies = {}
            for item in response.headers.headers:
                m = pat.match(item)
                if m:
                    cookies[m.group(r'name')] = m.group(r'value')
            self.cookies = cookies
            return ReturnData(response.code,cookies)
        except IOError,ex:
            return ReturnData(-1,ex.message)

    def close_session(self):
        if not self.cookies.has_key(r'LWSSO_COOKIE_KEY') or not self.cookies.has_key(r'QCSession'):
            return ReturnData(-1, r'')
        try:
            url = r'%s/qcbin/rest/site-session' % self.host
            cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;Path=/' % (self.cookies[r'LWSSO_COOKIE_KEY'],self.cookies[r'QCSession'])
            req_headers = {r'Cookie':cookiestring,r'Accept':'application/json'}
            req = urllib2.Request(url,data=None,headers=req_headers)
            req.get_method = lambda:'DELETE'
            response = urllib2.urlopen(req)
            return ReturnData(response.code, response.read())
        except IOError,ex:
            return ReturnData(-1,ex.message)

    def discard_token(self):
        try:
            url = r'%s/qcbin/authentication-point/logout' % self.host
            cookie = "LWSSO_COOKIE_KEY=%s" % self.token
            req_headers = {r'Cookie':cookie,}
            req = urllib2.Request(url,data=None,headers=req_headers)
            response = urllib2.urlopen(req)
            return ReturnData(response.code,r'')
        except Exception,ex:
            return ReturnData(-1,ex.message)

    def extend_session(self):
        if not self.cookies.has_key(r'LWSSO_COOKIE_KEY') or not self.cookies.has_key(r'QCSession'):
            return ReturnData(-1, r'')
        try:
            url = r'%s/qcbin/rest/site-session' % self.host
            cookiestring=r'LWSSO_COOKIE_KEY=%s;QCSession=%s;Path=/' % (self.cookies[r'LWSSO_COOKIE_KEY'],self.cookies[r'QCSession'])
            req_headers = {r'Cookie':cookiestring,}
            req = urllib2.Request(url,data=None,headers=req_headers)
            response = urllib2.urlopen(req)
            return ReturnData(response.code,response.read())
        except IOError,ex:
            return ReturnData(-1,ex.message)
