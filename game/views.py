from django.views import generic
from django.http import HttpResponseRedirect
from .models import Data
from django.shortcuts import render,HttpResponse
from datetime import datetime,date,timedelta

def index(request):
    return render(request, 'game/index.html')

def instructions(request):
    return render(request, 'game/base.html')

def gamepage(request):
    data = Data.objects.all()
    args=  {
        'data': data
    }
    return render(request, 'game/gamepage.html',args)


def policy(request):
    return render(request, 'game/policy.html')

def staticpage(request):
    return render(request, 'game/staticpage.html')

def newspage(request):
    return render(request, 'game/newspage.html')



 
def columnsChart(request):
    #统计所有来访公司来访次数的by month推移图(柱状堆叠图)
    #要画图第一步，获取行名和列名
    #列名: 获取visitCus中 所有来访公司的名字
    #行名: 获取所有数据库中的月份
    #数据：获取所有来访公司在数据库表中的count
 
    #首先获取列名：所有公司名称
    companys = Data.VisitCusInfo.objects.values("visitCompany__companyName").distinct()
    cols=[]
    for company in companys:
        if company["visitCompany__companyName"] not in cols:
            cols.append(company["visitCompany__companyName"])
    print(cols)
    #再来获取行名及数据
    dates = models.VisitCusInfo.objects.values("auditDate") #by客户稽核时间
    #对获取到的时间格式整理成by month,只获取月份
    rows = []
    for row in dates:
        month = row['auditDate'].strftime("%Y-%m")
        if month not in rows:
            rows.append(month)
    rows.sort()
    print(rows)
    #by月份 by公司获取每个公司访问次数
    #Echarts官网source参考： 获取legend
    # legend: {
    #     data:['直接访问','邮件营销','联盟广告','视频广告','搜索引擎','百度','谷歌','必应','其他']
    # },
    legend_data=cols
    #获取x轴数据，Echarts官网示例
    # xAxis : [
    #     {
    #         type : 'category',
    #         data : ['周一','周二','周三','周四','周五','周六','周日']
    #     }
    x_data = rows
    #获取数据内容，Echarts官网示例：
    # series : [
    #     {
    #         name:'直接访问',
    #         type:'bar',
    #         stack: '广告',
    #         data:[320, 332, 301, 334, 390, 330, 320]
    #     },
    #     {
    #         name:'邮件营销',
    #         type:'bar',
    #         stack: '广告',
    #         data:[120, 132, 101, 134, 90, 230, 210]
    #     },
    series=[]
    #rows存的是日期，cols存的是公司名
 
    for com in cols:
 
        serie = {"name":com,"type":"bar","stack":"访问次数","data":None}
        series_data = []
        for row in rows:
            cnt = models.VisitCusInfo.objects.filter(auditDate__year=row[0:4],auditDate__month=row[5:7],visitCompany__companyName=com).values("visitCompany__companyName").count()
            series_data.append(cnt)
        serie["data"]=series_data
        series.append(serie)
    #柱子宽度可以在这里设置,注意必须加在最后一个 'bar' 系列上才会生效，并且是对此坐标系中所有 'bar' 系列生效。
    series[-1]['barWidth']="40%"
    print(series)
 
    return render(request,"charts/visitChart.html",{"series":series,"x_data":x_data,"legend_data":legend_data})
