# coding=utf-8

import sys
import xml.etree.cElementTree as ET
if __name__=="__main__":
   for event, elem in ET.iterparse("all_lte_trace.xml", events=('end',)):#注意这里只使用end进行触发即可
         print(elem.tag, elem.text)

         if elem.tag == '{raml20.xsd}ps':
            a_result = {}
            a_result=elem.attrib
            a_result['value']=elem.text
            if(elem.text==None):
               print("result none")
            else:
               print(a_result)

         elif elem.tag=='{raml20.xsd}managedObject':
            print(elem.attrib)
         elem.clear()