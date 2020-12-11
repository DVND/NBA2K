# -*- coding: utf-8 -*-

# Data wrangling and math
import numpy as np
import pandas as pd 
from pylab import *
# Visualization tools
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')
# Datetime module
from datetime import datetime, date

df= pd.read_csv(r'C:\Users\Administrator\Desktop\python数据分析\nba2k20-full.csv')
t=df.head()
#print(t)
print('\n')

#去掉球员工资前面的美元符号
def get_salary(salary):
    salary=salary.replace('$',' ')
    return int(salary)

#找到最高评分和最低评分的球员
def find_most():
    best=df[df.rating==df.rating.max()].full_name
    print("最高评分球员列表:")
    print(best)
    print('\n')
    print("最低球员评分列表：")
    low=df[df.rating==df.rating.min()].full_name
    print(low)
    print('\n')
find_most()

#统计相同评分的球员数量
def same_values_column(column):
    same_distribution=df[[column,'full_name']].groupby(column).count().sort_values(by='full_name',ascending=False).reset_index()
    same_distribution.columns=[column,'number']
    print(f"球员中评分最多的数值是{same_distribution.rating[0]}")
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot(x=same_distribution.rating, y=same_distribution.number)
    plt.xticks(rotation=90)
    plt.xlabel('Rating value')
    plt.ylabel('Players count')
    plt.title('Most Rating Number')
    plt.show()   
#统计球员评分分布
same_values_column('rating')


#统计球员的国籍分布
def country_values_column(column):
    distribution=df[[column,'full_name']].groupby(column).count().sort_values(by='full_name',ascending=False).reset_index()
    distribution.columns=[column,'number']
    print(f"最多球员的国家是{distribution.country[0]}")
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot(x=distribution.country, y=distribution.number)
    plt.xticks(rotation=90)
    plt.xlabel('Country name')
    plt.ylabel('Players count')
    plt.title('Players country distribution')
    plt.show()
    
#统计球员国籍分布
country_values_column('country')

#统计每支球队人数的函数，column是列的名字,扇形统计图
def team_values_pie(column):
    distribution=df[[column,'full_name']].groupby(column).count().sort_values(by='full_name',ascending=False).reset_index()
    distribution.columns=[column,'number']
    print(f"最多球员的球队是{distribution.team[0]}")
     
    fig, ax = plt.subplots(figsize=(20,10))
    labels =np.array(distribution.team)   #对象转化为数组
    sizes = np.array(distribution.number)
    plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
    plt.title("Players team distribution")
    plt.show()

#调用函数观看各球队人数
team_values_pie('team')


#各球队的最高评分
def rating_values_line(column):
    distribution=df[[column,"team"]]    
    df1=df[[column,'team']].groupby('team').count().sort_values(by='team',ascending=False).reset_index()
    indexs=np.array(df1.team)   #生成球队名字列表
    a=[]
    for index in indexs:
        beat=distribution[distribution.team==index].rating.max()
        a.append(beat)
        print(f"{index}球队的球员最高评分是{beat}")
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot(x=indexs, y=a)
    plt.xticks(rotation=90)
    plt.xlabel('Team name')
    plt.ylabel('heighest rating')
    plt.title('Players heighest rating')
    plt.show()  

rating_values_line('rating')

#统计每年选修的球员人数
def draft_values_pie(column):
    distribution=df[[column,'full_name']].groupby(column).count().sort_values(by='full_name',ascending=False).reset_index()
    distribution.columns=[column,'number']
    print(f"选秀球员最多的年份是{distribution.draft_year[0]}")
     
    fig, ax = plt.subplots(figsize=(20,10))
    labels =np.array(distribution.draft_year)   #讲对象转化为数组
    sizes = np.array(distribution.number)
    plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
    plt.title("Players draft_year distribution")
    plt.show()

draft_values_pie('draft_year')

#统计球员位置数据
def position_values_pie(column):
    distribution=df[[column,'full_name']].groupby(column).count().sort_values(by='full_name',ascending=False).reset_index()
    distribution.columns=[column,'number']
    print(f"最多球员的位置是{distribution.position[0]}")
    
    fig, ax = plt.subplots(figsize=(20,10))
    labels =np.array(distribution.position)   #讲对象转化为数组
    sizes = np.array(distribution.number)
    plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
    plt.title("Players position distribution")
    plt.show()

position_values_pie('position')


#打印球员工资
def player_salary_column(column):
    df1=df[['full_name',column]]
    df1[column]=df1[column].apply(lambda x:get_salary(x))
    df1=df1.sort_values(by='salary',ascending=False).reset_index()
    print(df1)
    print(f"球员中最高薪资的是{df1['salary'].max()},薪资最高的球员是{df1[df1.salary==df1['salary'].max()].full_name}")
    print(f"球员中最低薪资的是{df1['salary'].min()},薪资最高的球员是{df1[df1.salary==df1['salary'].min()].full_name}")
    #打印统计图
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot(x=df1.full_name, y=df1.salary)
    plt.xticks(rotation=90)
    plt.xlabel('Players name')
    plt.ylabel('Players salary')
    plt.title('Players salary distribution')
    plt.show()
  
player_salary_column('salary')


#统计球队的工资帽
def team_salary_cap(column):
    distributions=df[[column,"team"]]
    df1=df[[column,'team']].groupby('team').count().sort_values(by='team',ascending=False).reset_index()
    indexs=np.array(df1.team)   #生成球队名字列表
    
    data=[]
    team_salary=0
    for index in indexs:
        for row in distributions.itertuples():
            if(getattr(row,'team')==index):
                team_salary+=get_salary(getattr(row,'salary'))
        data.append([index,team_salary])
        team_salary=0
    
    df2=pd.DataFrame(data)
    df2.columns=['team_name','salary_cap']
    print(f"工资帽最高的是{df2['salary_cap'].max()}")
    print(f"工资帽最低的是{df2['salary_cap'].min()}")
    print(df2)
    
    #打印统计图
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot(x=df2.team_name, y=df2.salary_cap)
    plt.xticks(rotation=270)
    plt.xlabel('Teams name')
    plt.ylabel('Salary cap')
    plt.title('Teams salary distribution')
    plt.show()

team_salary_cap('salary')


def highest_lowest_salary(column):
    dfs=df[[column,"team"]]
    df1=df[[column,'team']].groupby('team').count().sort_values(by='team',ascending=False).reset_index()
    indexs=np.array(df1.team)   #生成球队名字列表
    data=[]
    for index in indexs:
        dfs[dfs.team==index]
        mins=np.array(dfs[dfs.team==index])
        max_temp=0
        min_temp=get_salary(mins[0][0])
        for min in mins:
            if(max_temp<get_salary(min[0])):
                max_temp=get_salary(min[0])
            if(min_temp>get_salary(min[0])):
                min_temp=get_salary(min[0])
        data.append([index,min_temp,max_temp])
    t=pd.DataFrame(data)
    t.columns=["team","min_salary","max_salary"] 
    print(t)
    labels = ["Wizards","Jazz","Raptors","Spurs","Kings","Blazers","Suns","76ers","Magic",
              "Thunder","Knicks","Pelicans","Timberwolves","Bucks","Heat","Grizzles","Lakers",
              "Clippers","Pacers","Rockets","Warriors","Pistons","Nuggets","Mavericks",
              "Cavaliers","Bulls","Hornets","Nets","Celtics","Hawks"]
    max_salary = t.max_salary
    min_salary = t.min_salary

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(x - width/2, max_salary, width, label='Max')
    rects2 = ax.bar(x + width/2, min_salary, width, label='Min')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Salary')
    ax.set_title('Max and min salary')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    fig.tight_layout()
    plt.show()

highest_lowest_salary('salary')

#统计第一轮、第二轮和落选秀的分布
def draft_distribution(column):
    data=df[['full_name',column]]
    undraft_sum=0
    first_round=0
    second_round=0
    #计算第一轮、第二轮和落选秀
    for row in data.itertuples():
        if(getattr(row,'draft_peak')=='Undrafted'):
            undraft_sum+=1
        else:
            if(int(getattr(row,'draft_peak'))<=30):
                first_round+=1
            else:
                second_round+=1
    
    labels = ['First_round','Seconde_round','Undraft']
    values = [undraft_sum,first_round,second_round]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.show()
    print(undraft_sum)
    print(first_round)
    print(second_round)

draft_distribution('draft_peak')






