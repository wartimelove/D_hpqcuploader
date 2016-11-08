import urllib2,re
import json
from Parser import  HPQCParser
import Cred

class HPQCQuery:
    def __init__(self, project, domain):
        self.project = project
        self.domain = domain


    def get_pnp_test_set_id(self, path, pnp_name ,session):
        try:
            session.extend_session()
            folders = path.split(r'/')
            parent_id = 0
            for folder in folders:
                if folder:
                    ret_folders = self.enumerate_folder_private(parent_id, session)
                    if ret_folders == None:
                        return None
                    for ret_folder in ret_folders:
                        if ret_folder[1] == folder:
                            parent_id = ret_folder[0]
            testsets = self.enumerate_test_set_private(parent_id, session)
            if testsets == None:
                return  None
            test_set_id = None
            for testset in testsets:
                if testset[1] == pnp_name:
                    test_set_id = testset[0]
            return test_set_id

        except IOError:
            return None

    def get_test_instance_field(self,host,session):
        try:
                url = r'%s/qcbin/rest/domains/dcg/projects/bkc/customization/entities/test-instance/fields' % (host)
                cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                               (session.token,
                                session.cookies[r'QCSession'],
                                session.cookies[r'XSRF-TOKEN'])
                req_headers = {r'Cookie': cookiestring, r'Accept': r'application/xml'}


                req = urllib2.Request(url, data=None, headers=req_headers)
                req.add_header('Content-Type', 'application/xml')
                print 'url:',req.get_full_url()
                httpHandler = urllib2.HTTPHandler(debuglevel=1)
                httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
                opener = urllib2.build_opener(httpHandler, httpsHandler)
                urllib2.install_opener(opener)
                response = urllib2.urlopen(req)
                print  response.read()
        except Exception,e:
                print 'except', e
                import traceback
                traceback.print_exc()
                return None

    def get_all_test_case_id(self,test_set_id, session):
        try:
                result = []
                if test_set_id == None:
                    return result
                jsonobj = self.enumerate_test_instance_private(test_set_id, session)
                if jsonobj == None:
                    return None
                parser = HPQCParser()
                result = parser.ParseTestInstance(jsonobj)
                return result
        except Exception,e:
                import traceback
                traceback.print_exc()
                return None

    def create_test_instance_json(self,case_info, session):
        try:
                url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-instances' % (session.host)
                cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                               (session.token,
                                session.cookies[r'QCSession'],
                                session.cookies[r'XSRF-TOKEN'])
                req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}
                data = '''{"Fields":[{"Name":"status","values":[{"value":"%s"}]},
                                     {"Name":"iterations","values":[{"value":"%s"}]},
                                     {"Name":"exec-date","values":[{"value":"%s"}]},
                                     {"Name":"user-01","values":[{"value":"%s"}]},
                                     {"Name":"user-04","values":[{"value":"%s"}]},
                                     {"Name":"user-03","values":[{"value":"%s"}]},
                                     {"Name":"cycle-id","values":[{"value":"%s"}]},
                                     {"Name":"test-id","values":[{"value":"%s"}]},
                                     {"Name":"subtype-id","values":[{"value":"hp.qc.test-instance.MANUAL"}]},
                                     {"Name":"test-order","values":[{"value":"%s"}]}],"Type":"test-instance"}'''%\
                                    (case_info['status'],\
                                     case_info['iterations'],\
                                     case_info['exec_date'],\
                                     case_info['hsd_id'],\
                                     case_info['unit'], \
                                     case_info['value'],\
                                     case_info['test_set_id'],\
                                     case_info['test_case_id'],\
                                     case_info['test_case_order'])
                print data
                req = urllib2.Request(url, data=data, headers=req_headers)
                req.add_header('Content-Type', 'application/json')

                # httpHandler = urllib2.HTTPHandler(debuglevel=1)
                # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
                # opener = urllib2.build_opener(httpHandler, httpsHandler)
                # urllib2.install_opener(opener)
                response = urllib2.urlopen(req)
                return 1
        except Exception,e:
                import traceback
                traceback.print_exc()
                return -1


    def update_test_instance_json(self,case_info,session):
        try:
                url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-instances/%s' % (session.host, case_info['id'])
                cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                               (session.token,
                                session.cookies[r'QCSession'],
                                session.cookies[r'XSRF-TOKEN'])

                req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}


                data_str = '''{"Fields":[{"Name":"user-01","values":[{"value":"%s"}]},
                                        {"Name":"user-04","values":[{"value":"%s"}]},
                                        {"Name":"user-03","values":[{"value":"%s"}]},
                                        {"Name":"status","values":[{"value":"%s"}]},
                                        {"Name":"iterations","values":[{"value":"%s"}]},
                                        {"Name":"exec-date","values":[{"value":"%s"}]}],
                                        "Type":"test-instance"}'''%\
                                        (case_info['hsd_id'],
                                         case_info['unit'],
                                         case_info['value'],
                                         case_info['status'],\
                                         case_info['iterations'],\
                                         case_info['exec_date']\
                                         )


                req = urllib2.Request(url, data=data_str, headers=req_headers)
                req.add_header('Content-Type', 'application/json')
                # httpHandler = urllib2.HTTPHandler(debuglevel=1)
                # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
                # opener = urllib2.build_opener(httpHandler, httpsHandler)
                # urllib2.install_opener(opener)
                req.get_method = lambda:'PUT'
                response = urllib2.urlopen(req)
                # print response.read()
                return 1
        except Exception,e:
                print 'except', e
                import traceback
                traceback.print_exc()
                return -1

    def get_test_instance_json(self, instance_id,session):
        try:
                url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-instances/%s' % (session.host, instance_id)
                cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                               (session.token,
                                session.cookies[r'QCSession'],
                                session.cookies[r'XSRF-TOKEN'])

                req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}


                req = urllib2.Request(url, None, headers=req_headers)
                req.add_header('Content-Type', 'application/json')
                # httpHandler = urllib2.HTTPHandler(debuglevel=1)
                # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
                # opener = urllib2.build_opener(httpHandler, httpsHandler)
                # urllib2.install_opener(opener)

                response = urllib2.urlopen(req)
                print response.read()

        except Exception,e:
                print 'except', e
                import traceback
                traceback.print_exc()


    def enumerate_folder(self, path, session):
        try:
            session.extend_session()
            folders = path.split(r'/')
            parent_id = 0

            for folder in folders:
                if folder:
                    ret_folders = self.enumerate_folder_private(parent_id, session,0)
                    if ret_folders == None:
                        return None
                    for ret_folder in ret_folders:
                        if ret_folder[1] == folder:
                            parent_id = ret_folder[0]
            testsets = self.enumerate_folder_private(parent_id, session,0)
            if testsets == None:
                return  None
            return testsets
        except IOError:
            return None

    # def enumerate_test_instance_private(self, parent_folder, session):
    #     try:
    #         url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-instances/8255' % (
    #             session.host)
    #         print 'Url:', url
    #         cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
    #                        (session.token,
    #                         session.cookies[r'QCSession'],
    #                         session.cookies[r'XSRF-TOKEN'])
    #         req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}
    #         req = urllib2.Request(url, data=None, headers=req_headers)
    #         response = urllib2.urlopen(req)
    #         return json.load(response)
    #     except IOError:
    #         return None
    #     except Exception:
    #         return None

    def enumerate_test_instance_private(self, parent_folder, session):
        try:
            url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-instances?fields=test.name&query={cycle-id[%d]}' % (
                session.host, parent_folder)
            cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                           (session.token,
                            session.cookies[r'QCSession'],
                            session.cookies[r'XSRF-TOKEN'])
            req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}
            req = urllib2.Request(url, data=None, headers=req_headers)
            response = urllib2.urlopen(req)
            return json.load(response)
        except IOError:
            return None
        except Exception:
            return None

    def enumerate_test_set_private(self, parent_folder, session):
        try:

            url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-sets?query={parent-id[%d]}' % (
                    session.host, parent_folder)

            cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                           (session.token,
                            session.cookies[r'QCSession'],
                            session.cookies[r'XSRF-TOKEN'])
            req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}
            req = urllib2.Request(url, data=None, headers=req_headers)
            response = urllib2.urlopen(req)
            jsonobj = json.load(response)
            sets = []
            for entity in jsonobj[r'entities']:
                name = ''
                id = 0
                for field in entity['Fields']:
                    if field['Name'] == 'id':
                        id = int(field['values'][0]['value'])
                    if field['Name'] == 'name':
                        name = field['values'][0]['value']
                sets.append((id, name))
            return sets
        except IOError:
            return None
        except Exception:
            return None

    def enumerate_folder_private(self, parent, session):
        try:

            url = r'%s/qcbin/rest/domains/dcg/projects/bkc/test-set-folders?query={parent-id[%d]}' % (
                    session.host, parent)

            cookiestring = r'LWSSO_COOKIE_KEY=%s;QCSession=%s;XSRF-TOKEN=%s;Path=/' % \
                           (session.token,
                            session.cookies[r'QCSession'],
                            session.cookies[r'XSRF-TOKEN'])
            req_headers = {r'Cookie': cookiestring, r'Accept': r'application/json'}
            req = urllib2.Request(url, data=None, headers=req_headers)
            response = urllib2.urlopen(req)
            jsonobj = json.load(response)
            folders = []
            for entity in jsonobj[r'entities']:
                name = ''
                id = 0
                for field in entity['Fields']:
                    if field['Name'] == 'id':
                        id = int(field['values'][0]['value'])
                    if field['Name'] == 'name':
                        name = field['values'][0]['value']
                folders.append((id, name))
            return folders
        except IOError:
            return None
        except Exception:
            return None