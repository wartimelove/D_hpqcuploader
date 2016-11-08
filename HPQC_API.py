__author__ = 'kliux'

import Cred
import Query


def create_case_to_hpqc(case_info):
    try:
        host = r'https://hpalm.intel.com'
        query = Query.HPQCQuery('BKC', 'DCG')
        # session = Cred.Session(host, 'jtao5x', '')
        session = Cred.Session(host, 'ruipengx', '393728-hijk')
        # query.get_test_instance_field(host, session)
        #path = r'/Trash/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'], 'BKC')
        if case_info['hpqc_project'] == 'Grantley-Refresh':
            path = r'/%s/%s/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'][:4],'BDX',case_info['work_week'][-4:],'P&P')
        elif case_info['hpqc_project'] == 'Brickland_Refresh':
            path = r'/%s/%s/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'][:4],case_info['work_week'],'BDX','P&P')
        else:
            path = r'/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'],'P&P')
            print path
        test_set_id = query.get_pnp_test_set_id(path, case_info['test_set_name'], session)

        case_list = query.get_all_test_case_id(test_set_id,session)
        for case in case_list:
            if case_info['test_case_id'] == case[0]:
                #print exist test instance
                # query.get_test_instance_json(case[1],session)
                return 0

        case = {'value':case_info['test_case_value'],
                'unit':case_info['test_case_unit'],
                'test_set_id':test_set_id,
                'test_case_id':case_info['test_case_id'],
                'test_case_order':case_info['test_case_order'],
                'hsd_id':case_info['test_case_hsd'],
                'status':case_info['test_status'],
                'iterations':case_info['test_iterations'],
                'exec_date':case_info['test_exec_date']}
        result = query.create_test_instance_json(case, session)

        return result
    except Exception,e:
            print 'except', e
            import traceback
            traceback.print_exc()
            return None

def update_case_to_hpqc(case_info):
    try:
        host = r'https://hpalm.intel.com'
        query = Query.HPQCQuery('BKC', 'DCG')
        session = Cred.Session(host, 'ruipengx', '393728-hijk')

        #path = r'/Trash/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'],'P&P')
        if case_info['hpqc_project'] == 'Grantley-Refresh':
            path = r'/%s/%s/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'][:4],'BDX',case_info['work_week'][-4:],'P&P')
        elif case_info['hpqc_project'] == 'Brickland_Refresh':
            path = r'/%s/%s/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'][:4],case_info['work_week'],'BDX','P&P')
        else:
            path = r'/%s/%s/%s' % (case_info['hpqc_project'],case_info['work_week'],'P&P')


        test_set_id = query.get_pnp_test_set_id(path, case_info['test_set_name'], session)

        case_list = query.get_all_test_case_id(test_set_id,session)
        id = None
        for case in case_list:
            if case_info['test_case_id'] == case[0]:
                id = case[1]

        if not id:
           return -1

        case_info = {'value':case_info['test_case_value'],
                     'unit':case_info['test_case_unit'],
                     'id':id,
                     'hsd_id':case_info['test_case_hsd'],
                     'status':case_info['test_status'],
                     'iterations':case_info['test_iterations'],
                     'exec_date':case_info['test_exec_date']}
        result = query.update_test_instance_json(case_info, session)

        return result
    except Exception,e:
            print 'except', e
            import traceback
            traceback.print_exc()
            return None

