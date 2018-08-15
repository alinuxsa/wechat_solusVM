# coding:utf-8
import requests
import xml.etree.ElementTree as ET
from requests.packages import urllib3
urllib3.disable_warnings()
import os

class VPS():
    
    def __init__(self):
        self.api_key = os.getenv('API_KEY', '')
        self.api_hash = os.getenv('API_HASH', '')
        self.api_url = os.getenv('API_URL', \
                                 'https://myvm.hiformance.com/api/client/command.php')
    
    def __exec_api(self,**kwargs):
        #action = kwargs['action']
        payload = {'key':self.api_key,'hash':self.api_hash}
        payload = dict(payload,**kwargs)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(self.api_url,params=payload, verify=False, headers =
                         headers)
        return r.text
    def info(self):
        action_dic = {'action':'info','mem':'true','hdd':'true','bw':'true'}
        return self.__exec_api(**action_dic)
        """
        ipaddr (Returns a list of ipaddresses)
        hdd    (Returns the hard disk usage in Bytes) 
        mem    (Returns the memory usage in Bytes)
        bw     (Returns the bandwidth usage in Bytes)
        <ipaddr>123.123.123.123</ipaddr>
        <hdd>total,used,free,percentused</hdd> 
        <mem>total,used,free,percentused</mem>
        <bw>total,used,free,percentused</bw>
        """
        
    def status(self):
        action_dic = {'action':'status'}
        return self.__exec_api(**action_dic)

    def reboot(self):
        action_dic = {'action':'reboot'}
        return self.__exec_api(**action_dic)

    def boot(self):
        action_dic = {'action':'boot'}
        return self.__exec_api(**action_dic)
    
    def shutdown(self):
        action_dic = {'action':'shutdown'}
        return self.__exec_api(**action_dic)

def vmStatus():
    s1 = VPS()
    status = "<resp>{}</resp>".format(s1.status())
    info = "<resp>{}</resp>".format(s1.info())
    statusRoot = ET.fromstring(status)
    infoRoot = ET.fromstring(info)
    data = {}
    for statusElem in  statusRoot.iter():
        data.setdefault(statusElem.tag, statusElem.text)
    for infoElem in infoRoot.iter():
        data.setdefault(infoElem.tag, infoElem.text)
    return data

def vmctl(action):
	s1 = VPS()
	if action == 'boot':
		s1.boot()
	elif action == 'shutdown':
		s1.shutdown()
	elif action == 'reboot':
		s1.reboot()
	else:
		pass
			


if __name__ == '__main__':
    print(vmStatus())



