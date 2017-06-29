#coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from sqlalchemy import create_engine
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


#用sqlalchemy创建引擎  
sql = "select * from lte_day where instr(地市,'FDD')>0 "
engine = create_engine('mysql+pymysql://root:10300@192.168.3.74:50014/teee?charset=utf8')
#df.to_sql('tick_data',engine,if_exists='append')#存入数据库，这句有时候运行一次报错，运行第二次就不报错了，不知道为什么  
df1 = pd.read_sql(sql,engine)    #read_sql直接返回一个DataFrame对象      设置多个index，只要将index_col的值设置为列表

plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题




rrc = df1[['日期','地市','rrc建立成功率']]                            #取 '日期','地市','rrc建立成功率' 三列数据
rrcCity = rrc.pivot_table('rrc建立成功率', ['日期'], '地市')         # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
rrcFig = plt.figure(1,figsize=(8,4)) # Create a `figure' instance
rrcAx = rrcFig.add_subplot(111) # Create a `axes' instance in the figure
#Ax.plot(X1, Y1, X2, Y2) # Create a Line2D instance in the axes

rrcHandle = rrcAx.plot(rrcCity)    #根据dataFream rcCity 中的列 创建多条折线,其中X轴为索引  Y轴为多个列


'''                                  #设置标签,迭代handles 每一条线 逐个添加标签
i=0
for handle in rrcHandle:
    handle.set_label(rrcCity.columns[i])
    i+=1
'''

#erabAx.yaxis.set_major_formatter(DateFormatter('%m-%d'))  # 设置y轴主标签文本的格式
rrcAx.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))      #设置X时间显示格式
rrcAx.spines["right"].set_color("none")                       #设置右轴颜色为none
rrcAx.spines["top"].set_color("none")                       #设置上轴颜色为none
rrcAx.set_title("RRC建立成功率")                              #设置图表标题
rrcFig.autofmt_xdate()        #设置x轴时间外观
plt.ylim(98,100)
rrcAx.legend(rrcCity.columns,loc="best", ncol=1, shadow=True)


#rrcCity._info_axis.base

erab = df1[['日期','地市','erab建立成功率']]                            #取 '日期','地市','rrc建立成功率' 三列数据
erabCity = erab.pivot_table('erab建立成功率', ['日期'], '地市')         # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
erabFig = plt.figure(2,figsize=(8,4)) # Create a `figure' instance
erabAx = erabFig.add_subplot(111) # Create a `axes' instance in the figure
#Ax.plot(X1, Y1, X2, Y2) # Create a Line2D instance in the axes
erabHandle = erabAx.plot(erabCity) # Create a Line2D instance in the axes  根据erabCity画图



#erabAx.yaxis.set_major_formatter(DateFormatter('%m-%d'))  # 设置y轴主标签文本的格式
erabAx.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))      #设置X时间显示格式
erabAx.spines["right"].set_color("none")                       #设置右轴颜色为none
erabAx.spines["top"].set_color("none")                       #设置上轴颜色为none
erabAx.set_title("ERAB建立成功率")                              #设置图表标题
erabFig.autofmt_xdate()        #设置x轴时间外观
plt.ylim(99,100)
erabAx.legend(erabCity.columns,loc="best", ncol=3, shadow=True)
#erabFig.show()
#Fig.savefig("test.pdf")
print(0)







#rrcCanvas.print_figure('demo1.png')                           #保存为.png图片
plt.show()










'''
erab = df1[['日期','地市','erab建立成功率']]                            #取 '日期','地市','erab建立成功率' 三列数据
erabCity = erab.pivot_table('erab建立成功率', ['日期'], '地市')         # 数据列为 'erab建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
erabCity.plot(figsize=(10,5),title='ERAB建立成功率',rot=-20)
plt.legend(loc='lower right')                   #设置图例的位置
plt.ylim(99,100)                           #设置Y轴显示范围

#for a,b in zip(rrcCity.index,rrcCity.西安FDD):                                     #添加标签
#    plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)          #添加标签

'''