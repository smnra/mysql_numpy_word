#encoding=utf-8
from xml.etree import ElementTree

rualt = {}
def print_node(node):
    nodeDn = {'dn':'', 'lcr':'' }


    '''''打印结点基本信息'''
    #print("==============================================")
    #print("node.attrib:%s" % node.attrib)
    if 'class' in  node.attrib.keys() :
        if node.attrib['class'] == 'MTRACE' :
            nodeDn['dn'] =  node.attrib['distName']
            subNodes = node.findall("p")
            for subNode in  subNodes:
                if subNode.attrib['name'] == 'lcrId':
                    nodeDn['lcr'] = subNode.text
                    break
    return nodeDn

def read_xml(text):

    toFile = open('dn_lcr.csv', 'a')
    toFile.seek(0,0)
    toFile.write("dn,lcr\n")

    '''''读xml文件'''
    # 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）
    # root = ElementTree.parse(r"D:/test.xml")
    root = ElementTree.fromstring(text)


    # 获取element的方法
    # 1 通过getiterator
    lst_node = root.getiterator("managedObject")
    for node in lst_node:
        rualt = print_node(node)
        toFile.write(rualt['dn'] + ',' + rualt['lcr'] + '\n' )

        print(rualt['dn'] + ',' + rualt['lcr'])
    toFile.close()





    print(rualt)
    """
    # 2通过 getchildren
    lst_node_child = lst_node[0].getchildren()[0]
    print_node(lst_node_child)

    # 3 .find方法
    node_find = root.find('managedObject')
    print_node(node_find)

    #4. findall方法
    node_findall = root.findall("managedObject")[1]
    print_node(node_findall)

    """

if __name__ == '__main__':
     read_xml(open("movies.xml").read())