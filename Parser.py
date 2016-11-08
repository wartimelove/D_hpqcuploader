class HPQCParser:
    def ParseTestInstance(self,jsonobj):
        try:
            ret = []

            for entity in jsonobj[r'entities']:
                for field in entity['Fields']:
                    if field['Name'] == 'test-id' and field['values'] != [] and field['values'] != [{}]:
                        test_id = field['values'][0]['value']
                        continue
                    if field['Name'] == 'id' and field['values'] != [] and field['values'] != [{}]:
                        id = field['values'][0]['value']
                        continue
                ret.append([test_id, id])
            return ret
        except IOError:
            return None