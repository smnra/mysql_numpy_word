#coding=utf-8

from  datetime  import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from sqlalchemy import create_engine
from matplotlib.dates import AutoDateLocator, DateFormatter



def getMonthFirstDay():
    dt = datetime.today()                                                     #获取当前日期
    firstDate = dt.strftime("%Y%m") + '01'                                  #当前月第一天日期
    todayDate = dt.strftime("%Y%m%d")
    lastDate = datetime(dt.year,dt.month +1,1).strftime("%Y%m") + '01'      #下个月第一天日期
    return [firstDate,todayDate,lastDate]

tdate = getMonthFirstDay()
#用sqlalchemy创建引擎  
sql = "select * from wcdma_day where 地市 <>'其他'  AND   日期>= '" +tdate[0]  + "' AND 日期 <  '" + tdate[1]  + "'"
engine = create_engine('mysql+pymysql://root:10300@192.168.3.74:50014/3g_kpi_browsing?charset=utf8')
#df.to_sql('tick_data',engine,if_exists='append')#存入数据库，这句有时候运行一次报错，运行第二次就不报错了，不知道为什么  
df1 = pd.read_sql(sql,engine)    #read_sql直接返回一个DataFrame对象      设置多个index，只要将index_col的值设置为列表

filePath = os.getcwd() + '\\3G\\' + datetime.today().strftime("%Y%m%d") +  '\\'         #拼接文件夹以当天日期命名
if os.path.exists(filePath):                                                   #判断路径是否存在
    print(u"目标已存在:",filePath)                                                 #如果存在 打印路径已存在,
else:
    os.makedirs(filePath)                                                           #如果不存在 创建目录

writer = pd.ExcelWriter(filePath + tdate[0] + '_' + tdate[1] + '_WCDMA.xlsx')       #保存表格为excel      文件名称为本月起始日期_结束日期_WCDMA.xlsx
df1.to_excel(writer,'Sheet1')                                                                  #保存表格为excel
writer.save()                                                                                   #保存表格为excel


plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
plt.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题












class CreateChart:
    def createCharts(self,rrcCity,rowName,figIndex,yRange):
        self.rowName = rowName
        self.figIndex = figIndex
        self.yRange = yRange
        self.rrcCity = rrcCity
        self.rrcFig = plt.figure(self.figIndex,figsize=(8,5)) # Create a `figure' instance
        self.rrcAx = self.rrcFig.add_subplot(111) # Create a `axes' instance in the figure
        #Ax.plot(X1, Y1, X2, Y2) # Create a Line2D instance in the axes
        self.rrcAx.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))      #设置X时间显示格式
        self.rrcAx.set_xticks(pd.date_range(kpiCity.index[0],kpiCity.index[-1])) #设置x轴间隔
        self.rrcHandle = self.rrcAx.plot(self.rrcCity)    #根据dataFream rcCity 中的列 创建多条折线,其中X轴为索引  Y轴为多个列


        '''                                  #设置标签,迭代handles 每一条线 逐个添加标签
        i=0
        for handle in rrcHandle:
            handle.set_label(rrcCity.columns[i])
            i+=1
        '''

        self.rrcAx.spines["right"].set_color("none")                       #设置右轴颜色为none
        self.rrcAx.spines["top"].set_color("none")                       #设置上轴颜色为none
        self.rrcAx.set_title(self.rowName)                              #设置图表标题
        self.rrcFig.autofmt_xdate()                                    #设置x轴时间外观
        plt.ylim(self.yRange)                                            #Y轴 显示范围
        self.rrcAx.legend(self.rrcCity.columns,loc="lower center", shadow=True,bbox_to_anchor=(1.05,0.4) ,ncol=1)  #设置显示图例 以及图例的位置,级是否有阴影效果
        self.rrcFig.savefig(filePath + tdate[0] + '_' + tdate[1] + '_WCDMA_' + rowName + '.png')    #保存为 本月起始日期_结束日期_LTE_KPI名称.PNG图片







'''
df1['同频硬切换成功率(%)'] = df1['同频硬切换成功率(%)'].astype(np.float64)
kpi = df1[['日期','地市','同频硬切换成功率(%)']].fillna(0)                           #取 '日期','地市','rrc建立成功率' 三列数据
kpiCity = kpi.pivot_table('同频硬切换成功率(%)', ['日期'], '地市').sort_index(ascending=True)        # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
kpiChart = CreateChart()
kpiChart.createCharts(kpiCity,'同频硬切换成功率(%)','同频硬切换成功率(%)',(0,100))
'''






yRanges = ((99,100),(99,100),(99,100),(0,0.5),(0,0.5),(99,100),(0,100),(0,100),(75,100),(-110,-100),(0,10),(0,150000),(0,12000000),(0,1800000))


for i,kpiName in enumerate(df1.columns[2:]):                               #此种for语句 表示 遍历 列表df1.columns[2:],i为序号(1,2,3,4,5....)  kpiName 为列表df1.columns[2:]中的每一个元素
    df1[kpiName] = df1[kpiName].astype(np.float64)                          #类型转换,将列转换为 float64 类型
    kpi = df1[['日期','地市',kpiName]].fillna(0)                           #取 '日期','地市','rrc建立成功率' 三列数据
    kpiCity = kpi.pivot_table(kpiName, ['日期'], '地市').sort_index(ascending=True)        # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
    kpiChart = CreateChart()
    kpiChart.createCharts(kpiCity,kpiName,kpiName,yRanges[i])





#plt.show()









'''
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
'''









