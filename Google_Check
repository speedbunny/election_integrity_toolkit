import googlesearch
from contextlib import redirect_stdout
#from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
#from proxy_requests import ProxyRequests, ProxyRequestsBasicAuth
#from proxy_requests import requests
#import pytest
#from socket import inet_aton

#r = ProxyRequests('https://api.ipify.org')
#assert r.get_status_code() == 200
#r.get()
#try:
#    inet_aton(r.__str__())
#except Exception:
#    pytest.fail('Invalid IP address in response')
filepath = 'fails.txt'
with open(filepath) as fp:
 line = fp.readline()
 cnt = 1
 while line:
       line = fp.readline()
       hn = line.split()[0]
       hns=str(hn)
       results=googlesearch.search("\""+line+"\""+" NV", tld='com', lang='en', tbs='0', safe='off', num=1, start=0, stop=1, pause=5.0, country='', extra_params=None, user_agent=None, verify_ssl=True)
       res=list(results)
       print(line)
       print(res)
       ress=str(res)
       cnt += 1
       zillow = "zillow"
       realtor="redfin"
       if not hns in ress:
           print('second check')
           if not zillow or not realtor in ress:
               print('logging')
               with open('failr.txt', 'a') as f:
                 with redirect_stdout(f):
                  print(line)
                  print(res)
