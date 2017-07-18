# coding=utf-8

import sys
import xml.etree.cElementTree as ET
class readXMLET():
    def __init__(self):
        self.p = {}
        self.title = []
        self.buff=[]

    def readXML(self,xmlPath):
        objectNum = 0
        toFile = open('write.csv' ,'w+')                                             #以追加的方式打开文件write.csv
        for event, elem in ET.iterparse(xmlPath, events=('end',)):             #注意这里只使用end进行触发即可
            self.line=[]                                                         # 清空self.line
            if elem.tag == '{raml20.xsd}p' and elem.attrib != {}:                   #如果标签的为 p 或者标签的属性为空
                self.p[elem.attrib[list(elem.attrib)[0]]] = elem.text                  #将elem.attrib[list(elem.attrib)[0]] 为key elem.text 为value 的对象 存储进字典P

                if not (elem.attrib[list(elem.attrib)[0]] in self.title):       #如果title中不存在key 则添加key到title中
                    self.title.append(elem.attrib[list(elem.attrib)[0]])         # 以上为处理P标签

                if(elem.text==None):                                                #空标签处理
                    print("result none")
                else:
                    pass

            elif elem.tag=='{raml20.xsd}managedObject':                        #managedObject标签处理

                self.p.update(elem.attrib)                                          #把字典elem.attrib 合并到self.p中

                for key,value in self.p.items():
                    if not (key in self.title):                                     #如果self.title中不存在key 则添加key到title中
                        self.title.append(key)

                for key in self.title:                                              # 遍历self.title列表 以列表的每一项为key,在字典self.p 中 取value的值 写入列表self.buff
                    #self.line.append(self.p[key])
                    self.line.append(self.p.get(key,'_'))                #如果key 不存在 则写入默认值 '__'
                self.line[-1]=self.line[-1] + '\n'                                            #向最后一个元素加上换行符号\n
                objectNum += 1                                                       #每一次遇到managedObject 标签结束时,使objectNum 变量加一
            #print(self.line)
            if self.line != []  and self.line[self.title.index('class')] == "MTRACE" :          #self.title.index('class') 为列表self.title中元素 "class" 的索引值(位置)   表示当self.line的class 元素为 "MTRACE"时
                self.buff.append(list(self.line))             #每次循环完成, 将self.line 添加为 self.buff的一个元素  list(self.line) 为创建一个self.line列表的深拷贝
                self.line.clear()                       #每次循环完成清空self.line列表
                #print(self.buff)
            elem.clear()                            #清楚标签

            if objectNum == 100:                    #如果objectNum等于100,
                for tofileline in  self.buff:       #迭代self.buff,的每一项
                    tmp = list(map(lambda x: x + ',', tofileline))      #使用map函数 给tofileline列表的每一项都增加字符 ','
                    tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
                    toFile.writelines(tmp)        #写入tmp列表 到文件toFile中

                #toFile.flush()                      #立即写入缓冲区文件
                self.buff.clear()                   #清空self.buff列表
                objectNum = 0                       #复位objectNum变量

        for tofileline in  self.buff:       #迭代self.buff,的每一项
            tmp = list(map(lambda x: x + ',', tofileline))      #使用map函数 给tofileline列表的每一项都增加字符 ','
            tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
            toFile.writelines(tmp)        #写入tmp列表 到文件toFile中

        #toFile.seek(0,0)                                        #将文件指针移动到文件第一行第一个字符,即将写入文件标题
        #if not (toFile.tell()):
        tmp = list(map(lambda x: x + ',', self.title))      #使用map函数 给self.title列表的每一项都增加字符 ','
        tmp[-1] = tmp[-1][:-1]                                # 是tofileline 列表的最后一项去掉最后一个字符 ','
        toFile.writelines(tmp)        #写入tmp列表 到文件toFile中,(将标题写入文件最后一行)

        print("Over!")
        toFile.close()                           #关闭文件
if __name__=="__main__":
    readxml = readXMLET()
    readxml.readXML("all_lte_trace.xml")