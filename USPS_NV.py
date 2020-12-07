#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Nevada Voter list against USPS delivery addresses.
Note USPS returns false negatives and those need to go for secondary checks
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 02:58:44 2020

@author: Sarah Eaglesfield
"""
import pandas as pd
from usps import USPSApi, Address
from contextlib import redirect_stdout

NV_read = pd.read_csv("in.csv", delimiter = ',',usecols = ['RES_UNIT','RES_STREET_NUM','RES_DIRECTION','RES_STREET_NAME','RES_ADDRESS_TYPE','RES_CITY','RES_ZIP_CODE'])
for row,column in NV_read.iterrows():
      streetu=column["RES_UNIT"]
      streetn=column["RES_STREET_NUM"]
      streetd=column["RES_DIRECTION"]
      streetnm=column["RES_STREET_NAME"]
      streett=column["RES_ADDRESS_TYPE"]
      cityz=column["RES_CITY"]
      zipcodez=column["RES_ZIP_CODE"]
      trw=str(streetn)
      streetnum=str(trw.replace(".0",""))
      if pd.isnull(streetu):
          units=str(" ")
      else:
         units=str(streetu)
      if pd.isnull(streett):
         stype=str(" ")
      else:
         stype=str(streett)
      if pd.isnull(streetd):
          fulladdress=[str(streetnum), str(streetnm), str(stype)]
      else:
          fulladdress=[str(streetnum),str(streetd),str(streetnm),str(stype)]
      x=' '.join(fulladdress)
      firstline = str(x.replace("  ", " ")+".")
      citys=str(cityz)
      zipcodes=str(zipcodez)
      address = Address(
      name='Tobin Brown',
      address_1=units,
      address_2=firstline,
      city=citys,
      state='NV',
      zipcode=zipcodes
     )
      usps = USPSApi('857STUDE6453', test=True)
      validation = usps.validate_address(address)
      valids=str(validation.result)
      print(firstline)
      print(validation.result)
      checkerror = "Error"
#      Uncomment to report default addresses      
#      defaults = "Default"
#      if checkerror in valids or defaults in valids:
      if checkerror in valids:
             with open('out.txt', 'a') as f:
                with redirect_stdout(f):
                  print(firstline)
                  print(validation.result)
