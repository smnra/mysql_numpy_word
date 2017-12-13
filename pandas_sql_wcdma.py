#coding=utf-8

from  datetime  import datetime
import arrow
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from sqlalchemy import create_engine
from matplotlib.dates import AutoDateLocator, DateFormatter



def getDateRange():
    '''
    #获取参数(默认为当天)所在月份的第一个完整周 周一的日期
    '''
    now = arrow.now()                                                        #当前时间
    rangeDate={}                                                             #定义返回值  字典
    rangeDate['today'] = arrow.now().format('YYYYMMDD')                 #今日的日期

    lastMonth_1st_day = now.floor('month').replace(months = -1)             #上个月1号的日期
    thisMonth_1st_day = now.floor('month')                                  #这个月1号的日期
    nextMonth_1st_day = now.floor('month').replace(months = +1)             #下个月1号的日期
    lastWeek_Monday = now.replace(weeks = -1).floor('week')             #上一周周一的日期
    thisWeek_Monday = now.floor('week')                                 #这一周周一的日期
    if thisMonth_1st_day.isoweekday() == 1 :                                #如果这个月的1号是周一,
        thisMonth_1st_Monday = now.floor('month')                           #则这个月的第一个完整周 的 周一的日期 就是当月的1号的日期
    else :
        thisMonth_1st_Monday = now.floor('month').replace(weeks = +1).floor('week')      #否则这个月的第一个完整周 的 周一的日期 就是当月1号所在的下一周的周一的日期

    if thisWeek_Monday - thisMonth_1st_Monday == thisWeek_Monday - thisWeek_Monday :       #如果 这一周周一的日期  减去这个月的第一个完整周 周一的日期 如果结果等于0
        rangeDate['startDate'] = lastMonth_1st_day.format('YYYYMMDD')               #开始时间就是上个月1号
        rangeDate['endDate'] = thisMonth_1st_Monday.format('YYYYMMDDH')               #结束时间就是这个月的第一个完整周 周一的日期
    else :
        rangeDate['startDate'] = thisMonth_1st_day.format('YYYYMMDD')               #开始时间就是这个月1号
        rangeDate['endDate'] = nextMonth_1st_day.format('YYYYMMDD')                 #结束时间就是这个月的第一个完整周 周一的日期

    return rangeDate


tdate = getDateRange()
#用sqlalchemy创建引擎
sql = "select * from city_wcdma_day where 地市 <>'其他'  AND   日期>= %s AND 日期 <  %s"  %(tdate['startDate'],tdate['endDate'])
engine = create_engine('mysql+pymysql://root:10300@192.168.3.74:50014/3g_kpi_browsing?charset=utf8')
#df.to_sql('tick_data',engine,if_exists='append')#存入数据库，这句有时候运行一次报错，运行第二次就不报错了，不知道为什么  
df1 = pd.read_sql(sql,engine)    #read_sql直接返回一个DataFrame对象      设置多个index，只要将index_col的值设置为列表

filePath = os.getcwd() +  '\\' + datetime.today().strftime("%Y%m%d")  + '\\3G\\'        #拼接文件夹以当天日期命名
if os.path.exists(filePath):                                                   #判断路径是否存在
    print(u"目标已存在:",filePath)                                                 #如果存在 打印路径已存在,
else:
    os.makedirs(filePath)                                                           #如果不存在 创建目录

writer = pd.ExcelWriter(filePath + tdate['startDate'] + '_' + tdate['today'] + '_WCDMA.xlsx')       #保存表格为excel      文件名称为本月起始日期_结束日期_WCDMA.xlsx
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
        self.rrcFig.savefig(filePath + tdate['startDate'] + '_' + tdate['endDate'] + '_WCDMA_' + rowName + '.png')    #保存为 本月起始日期_结束日期_LTE_KPI名称.PNG图片







'''
df1['同频硬切换成功率(%)'] = df1['同频硬切换成功率(%)'].astype(np.float64)
kpi = df1[['日期','地市','同频硬切换成功率(%)']].fillna(0)                           #取 '日期','地市','rrc建立成功率' 三列数据
kpiCity = kpi.pivot_table('同频硬切换成功率(%)', ['日期'], '地市').sort_index(ascending=True)        # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
kpiChart = CreateChart()
kpiChart.createCharts(kpiCity,'同频硬切换成功率(%)','同频硬切换成功率(%)',(0,100))
'''






yRanges = ((99,100),(99,100),(99,100),(0,0.5),(0,0.5),(99,100),(25,55),(0,100),(75,100),(-110,-100),(0,10),(0,8000),(0,800000),(0,100000))


for i,kpiName in enumerate(df1.columns[2:]):                               #此种for语句 表示 遍历 列表df1.columns[2:],i为序号(1,2,3,4,5....)  kpiName 为列表df1.columns[2:]中的每一个元素
    df1[kpiName] = df1[kpiName].astype(np.float64)                          #类型转换,将列转换为 float64 类型
    kpi = df1[['日期','地市',kpiName]].fillna(0)                           #取 '日期','地市','rrc建立成功率' 三列数据
    kpiCity = kpi.pivot_table(kpiName, ['日期'], '地市').sort_index(ascending=True)        # 数据列为 'rrc建立成功率', '日期' 列不变,把 '地市'这一列 按照内容转换为多列
    kpiChart = CreateChart()
    kpiChart.createCharts(kpiCity,kpiName,kpiName,yRanges[i])




