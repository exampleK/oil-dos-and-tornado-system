
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import tornado.ioloop
from tornado.web import RequestHandler,StaticFileHandler
import pymysql,os
from pymysql import cursors
import xlrd #read execl
import sys
import datetime,time
list_temp_sql_result = []
list_temp_sql_result2 = []

class SelectHandler(tornado.web.RequestHandler):
    def by_name(self,t):
        return(t[0])
    def calu_oil_L(self,oil_H):
        import math
        oil_R = 1.2
        oil_L = 6.05
        oil_C = 0.6
        L = (oil_L*((math.pi * oil_R**2)/2-(oil_R-oil_H)*math.sqrt(2*oil_H*oil_R-oil_H**2)-oil_R**2*math.asin(1-oil_H/oil_R))+(math.pi*oil_C)/(3*oil_R)*(3*oil_R**2*oil_H-oil_R**3+(oil_R-oil_H)**3))
        return L
    def get(self):
        global list_temp_sql_result,list_temp_sql_result2
        list_temp_sql_result = []
        list_temp_sql_result2 = []
        
        # 查数据
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
        cursor = conn.cursor()

        temp1 = "select * from boom_car"
        cursor.execute(temp1)
        temp_sql_result1 = cursor.fetchall()
        boom_date = ((max(temp_sql_result1))[0])
        boom_car_scale = ((max(temp_sql_result1))[-1])
        conn.commit()

        temp2 = "select * from nor_car"
        cursor.execute(temp2)
        temp_sql_result2 = cursor.fetchall()
        nor_date = ((max(temp_sql_result2))[0])
        nor_car_scale = ((max(temp_sql_result2))[-1])
        conn.commit()

        # boom_car
        temp1 = "select * from boom_car"
        cursor.execute(temp1)
        temp_sql_result = cursor.fetchall()
        # list_temp_sql_result = []
        for i in temp_sql_result:
            list_temp_sql_result.append(i)

        # nor_car
        temp2 = "select * from nor_car"
        cursor.execute(temp2)
        temp_sql_result2 = cursor.fetchall()
        list_temp_sql_result2 = []
        for i in temp_sql_result2:
            list_temp_sql_result2.append(i)

        list_temp_sql_result = (sorted(list_temp_sql_result, key=self.by_name))
        list_temp_sql_result2 = (sorted(list_temp_sql_result2, key=self.by_name))
        # print(list_temp_sql_result)
        # print(list_temp_sql_result2)
        
        
        # oil_high
        temp5 = "select * from oil_high where id=(select max(id) from oil_high)"

        # cur = conn.cursor(cursorclass=pymysql.cursors.DictCursor)
        cursor.execute(temp5)
        list_temp_sql_result5 = []
        for i in cursor.fetchall():
            for ii in i:
                list_temp_sql_result5.append(ii)
        from math import ceil, floor

        oil_h1_p = (ceil((self.calu_oil_L(float(list_temp_sql_result5[1])))/30.989*100))
        oil_h2_p = (ceil((self.calu_oil_L(float(list_temp_sql_result5[2])))/30.989*100))
        # --->

        # <-- mysql(oil_execl) date --- sum --- sum_ava --- oil_sum_p --- today_p
        temp_oil_execl = "select * from oil_execl"
        cursor.execute(temp_oil_execl)
        temp_sql_result_oil_execl = cursor.fetchall()

        list_temp_sql_result_oil_execl = []
        for i in temp_sql_result_oil_execl:
            list_temp_sql_result_oil_execl.append(i)
        list_temp_sql_result_oil_execl = (sorted(list_temp_sql_result_oil_execl, key=self.by_name))
        # print("*"*10,list_temp_sql_result_oil_execl[-1][0]) #date
        # print("*"*10,list_temp_sql_result_oil_execl[-1][1]) #sum
        # print("*"*10,list_temp_sql_result_oil_execl[-1][2]) #sum_ava
        # print("*"*10,list_temp_sql_result_oil_execl[-1][3]) #oil_sum_p
        # print("*"*10,list_temp_sql_result_oil_execl[-1][-1]) #today_p
        oil_sum = (ceil(float(list_temp_sql_result_oil_execl[-1][1])))
        print(oil_sum)
        oil_sum_date = list_temp_sql_result_oil_execl[-1][0]
        today_p = list_temp_sql_result_oil_execl[-1][-1]
        oil_sum_p = list_temp_sql_result_oil_execl[-1][3]

                 
        # -->
        # <--查询最近的油量不为0的一条记录
        temp4 = "select * from income_oil"
        cursor.execute(temp4)
        temp_sql_result4 = cursor.fetchall()

        list_temp_sql_result4 = []
        for i in temp_sql_result4:
            list_temp_sql_result4.append(i)
        list_temp_sql_result4 = (sorted(list_temp_sql_result4, key=self.by_name))

        for i in range(10,1,-1):
            if (list_temp_sql_result4[i][1]) != str(0):
                income_i = i
                break
        # print(list_temp_sql_result4[income_i][0])
        # print(list_temp_sql_result4[income_i][1])
        # -->

        cursor.close()
        conn.close()
        # names = locals()
        '''
        for i in range(11):
            print(i)
            date = (list_temp_sql_result[i][0].strftime("%Y-%m-%d"))
            globals()['date' + str(i)] = ("'%s'"%date)
            globals()['boom' + str(i)] = list_temp_sql_result[i][2]
            globals()['nor' + str(i)] = list_temp_sql_result2[i][2]
            # names['date%s' % i] = list_temp_sql_result[i][0]
            # names['boom%s' % i] = list_temp_sql_result[i][2]
            # names['nor%s' % i] = list_temp_sql_result2[i][2]
        print(list_temp_sql_result[income_i][-1])
        '''
        self.render('index.html',oil_sum = oil_sum,today_p = today_p,oil_sum_p = oil_sum_p,oil_sum_date = oil_sum_date,\
            yewei_date = (list_temp_sql_result5[0]),oil_h1_p=(oil_h1_p),oil_h2_p=(oil_h2_p),boom_date = boom_date,boom_car_scale=boom_car_scale,\
            nor_date = nor_date,nor_car_scale=nor_car_scale,\
            income_date = (list_temp_sql_result4[income_i][0]),income_scale=(list_temp_sql_result4[income_i][-1]),\
            date0 = ("'%s'"%((list_temp_sql_result[-11][0]).strftime("%Y-%m-%d"))),date1 = ("'%s'"%((list_temp_sql_result[-1][0]).strftime("%Y-%m-%d"))),date2 = ("'%s'"%((list_temp_sql_result[-2][0]).strftime("%Y-%m-%d"))),date3 = ("'%s'"%((list_temp_sql_result[-3][0]).strftime("%Y-%m-%d"))),date4 = ("'%s'"%((list_temp_sql_result[-4][0]).strftime("%Y-%m-%d"))),date5 = ("'%s'"%((list_temp_sql_result[-5][0]).strftime("%Y-%m-%d"))),date6 = ("'%s'"%((list_temp_sql_result[-6][0]).strftime("%Y-%m-%d"))),date7 = ("'%s'"%((list_temp_sql_result[-7][0]).strftime("%Y-%m-%d"))),date8 = ("'%s'"%((list_temp_sql_result[-8][0]).strftime("%Y-%m-%d"))),date9 = ("'%s'"%((list_temp_sql_result[-9][0]).strftime("%Y-%m-%d"))),date10 = ("'%s'"%((list_temp_sql_result[-10][0]).strftime("%Y-%m-%d"))),\
            boom0 = list_temp_sql_result[-11][2],boom1 = list_temp_sql_result[-1][2],boom2 = list_temp_sql_result[-2][2],boom3 = list_temp_sql_result[-3][2],boom4 = list_temp_sql_result[-4][2],boom5 = list_temp_sql_result[-5][2],boom6 = list_temp_sql_result[-6][2],boom7 = list_temp_sql_result[-7][2],boom8 = list_temp_sql_result[-8][2],boom9 = list_temp_sql_result[-9][2],boom10 = list_temp_sql_result[-10][2],\
            nor0 = list_temp_sql_result2[-11][2],  nor1 = list_temp_sql_result2[-1][2],nor2 = list_temp_sql_result2[-2][2],nor3 = list_temp_sql_result2[-3][2],nor4 = list_temp_sql_result2[-4][2],nor5 = list_temp_sql_result2[-5][2],nor6 = list_temp_sql_result2[-6][2],nor7 = list_temp_sql_result2[-7][2],nor8 = list_temp_sql_result2[-8][2],nor9 = list_temp_sql_result2[-9][2],nor10 = list_temp_sql_result2[-10][2],)
        

    def post(self, *args, **kwargs):
        '''
        username = self.get_argument('username',None)
        pwd = self.get_argument('pwd', None)
 
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
        cursor = conn.cursor()
 
        # %s 要加上'' 否则会出现KeyboardInterrupt的错误
        #temp = "select name from userinfo where name='%s' and password='%s'" % (username, pwd)
        #temp = "INSERT INTO userunfo VALUES('%s','%s')"%(username, pwd)
        #temp = "DELETE FROM userinfo WHERE username='%s'"%(username, pwd)
        temp1 = "select name from userinfo"
        #effect_row = cursor.execute(temp)
        effect_row1 = cursor.execute(temp1)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        for x in result:
            print (x)
        '''
        self.render('poem.html', roads='123')
        '''
        if result:
            self.write('成功')
        else:
            self.write('失败！')
        '''
class dluHandler(tornado.web.RequestHandler):
    boom_car_dict = {}
    nor_car_dict = {}
    income_dict = {}
    def get(self):
        self.render("dlu.html")
    def post(self):
        file_metas = self.request.files["fafafa"]               #获取上传文件信息
        for meta in file_metas:                                 #循环文件信息
            file_name = meta['filename']                        #获取文件的名称
            import os                                           #引入os路径处理模块
            file_name = os.path.join(os.path.dirname(__file__),'static','upload_execl',file_name)
            #os拼接文件保存路径，以字节码模式打开
            with open(file_name,'wb') as up:
                #将文件写入到保存路径目录
                up.write(meta['body'])
        print(file_name)
        # 读取文件
        data = xlrd.open_workbook(file_name)
        # 通过索引顺序获取 ：sheet 0 就是第一个
        table = data.sheets()[0]
        table.col_values(0)
        # 找sum总和
        test_list1=[]
        list_temp =[]

        for i in range(len(table.col_values(10)),3,-1):
            # 1 判断12天内的数据，采用自减也就是从后到前，因为更新是自下而上
            # 2 判断总和的话都可以
            # 3 前面3行不要，所以到3结束
                # print(i)
                # print(table.col_values(10)[i-1])
                test_list1.append(table.col_values(10)[i-1])
                if table.col_values(2)[i-1] == ((datetime.date.today()+datetime.timedelta(-12)).strftime("%Y.%m.%d")):
                    list_temp.append(i-1)
                
        # print(min(list_temp))
        ii = min(list_temp)+1
        # print(table.col_values(2)[ii])
        # print(sum(test_list1))
        for x in range(12,0,-1):
            # print(x)
            boom_list = []
            nor_list =[]
            income_list =[]
            curr_date = ((datetime.date.today()+datetime.timedelta(-x)).strftime("%Y.%m.%d"))        
            while ((ii !=  len(table.col_values(10))) and (table.col_values(2)[ii] == curr_date)):
                    # 将当前日期定义成一个变量，减少反复的复用
                    # curr_date = ((datetime.date.today()+datetime.timedelta(-x)).strftime("%Y.%m.%d"))
                    # 判断语句
                    if table.col_values(3)[ii] == "地面站":
                        boom_list.append((table.col_values(9))[ii])

                        # print(curr_date,":",table.col_values(4)[i],":",(table.col_values(9))[i])
                    elif table.col_values(3)[ii] == "车队":
                        # 向车队list添加当天的所有list
                        nor_list.append((table.col_values(9))[ii])
                        # print(curr_date+":"+table.col_values(4)[i],":",(table.col_values(9))[i])
                    elif table.col_values(3)[ii] == "新疆卓信投资有限公司吉木萨尔县矿区加油站":
                        income_list.append(table.col_values(9)[ii])
                        # print(table.col_values(9)[i])
                    else:
                        # 可写当i和x的时候有未知错误
                        continue
                    ii=ii+1
                    # print(ii)
            # 组成一个完整的dict
            self.boom_car_dict[curr_date] = boom_list
            self.nor_car_dict[curr_date] = nor_list
            self.income_dict[curr_date] = income_list
        print(sum(test_list1))
            # today_lose_boom = (boom_car_dict[((datetime.date.today()+datetime.timedelta(-1)).strftime("%Y.%m.%d"))])
            # today_lose_nor = (nor_car_dict[((datetime.date.today()+datetime.timedelta(-1)).strftime("%Y.%m.%d"))])
            # from math import ceil
            # today_lose_sum_p = (ceil(sum(today_lose_boom)+sum(today_lose_nor))/sum(test_list1)*100)
            # sum_p = (ceil((test_list1)/(30.989*2*100)))
        # 
        date1 = ((datetime.date.today()+datetime.timedelta(-1)).strftime("%Y.%m.%d"))
        today_lose_boom = (self.boom_car_dict[((datetime.date.today()+datetime.timedelta(-1)).strftime("%Y.%m.%d"))])
        today_lose_nor = (self.nor_car_dict[((datetime.date.today()+datetime.timedelta(-1)).strftime("%Y.%m.%d"))])
        from math import ceil
        today_lose_sum_p = (ceil(((sum(today_lose_boom)+sum(today_lose_nor))/(30989*2))*100))
        sum_p = (ceil((sum(test_list1))/(30989*2)*100))

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
        cursor = conn.cursor()
        temp = "INSERT IGNORE INTO oil_execl (date,sum,sum_ava,oil_sum_p,today_percent) VALUES('%s','%s','%s','%s','%s')"%(date1,sum(test_list1),sum(test_list1)-7000,sum_p,today_lose_sum_p)
        cursor.execute(temp)
        print("269")
        cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()

        for i in self.nor_car_dict:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
            cursor = conn.cursor()
            temp = "INSERT IGNORE INTO nor_car (data,oil_scale) VALUES('%s','%s')"%(i,sum(self.nor_car_dict[i]))
            cursor.execute(temp)
            print("282")
            # cursor.execute(temp1)
            cursor.fetchall()
            # print((max(temp_sql_result))[0])
            # print((max(temp_sql_result))[-1])
            conn.commit()
            cursor.close()
            conn.close()

        for i in self.boom_car_dict:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
            cursor = conn.cursor()
            temp = "INSERT IGNORE INTO boom_car (data,oil_scale) VALUES('%s','%s')"%(i,sum(self.boom_car_dict[i]))
            cursor.execute(temp)
            print("296")
            # temp_sql_result = cursor.fetchall()

            conn.commit()
            cursor.close()
            conn.close()

        for i in self.income_dict:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
            cursor = conn.cursor()
            temp = "INSERT IGNORE INTO income_oil (data,oil_scale) VALUES('%s','%s')"%(i,sum(self.income_dict[i]))
            print("307")
            cursor.execute(temp)
            cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
        # time.sleep(3)
        # self.redirect("/alertindex.html")
        self.render("alertindex.html")

    '''
    def by_shengxu(self,t):
        # 配合sort升序list的函数
        return(t[0])
    '''

class CalcuHandler(tornado.web.RequestHandler):
    def by_shengxu(self,t):
        return(t[0])
    def calu_oil_L(self,oil_H):
        import math
        oil_R = 1.2
        oil_L = 6.05
        oil_C = 0.6
        L = (oil_L*((math.pi * oil_R**2)/2-(oil_R-oil_H)*math.sqrt(2*oil_H*oil_R-oil_H**2)-oil_R**2*math.asin(1-oil_H/oil_R))+(math.pi*oil_C)/(3*oil_R)*(3*oil_R**2*oil_H-oil_R**3+(oil_R-oil_H)**3))
        return L
    def get(self):
        # 两个文本框 一个提交按钮 ，post提交后转入tornado post方法
        '''
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
        cursor = conn.cursor()
        temp1 = "select * from oil_high where id=(select max(id) from oil_high)"
        cursor.execute(temp1)
        temp_sql_result1 = cursor.fetchall()
        list_temp_sql_result5 = []
        for i in temp_sql_result1:
            list_temp_sql_result5.append(i)
        list_temp_sql_result5 = (sorted(list_temp_sql_result5, key=self.by_shengxu))
        print((max(temp_sql_result1))[0])
        print((max(temp_sql_result1))[-1])
        # oil_date = (((temp_sql_result1))[0])
        # boom_car_scale = (((temp_sql_result1))[-1])
        conn.commit()
        cursor.close()
        conn.close()
        # self.render('yewei1.html', oil_h1=oil_h1,oil_h2=oil_h2,oil_sum=oil_sum,oil_sum_ava=oil_sum_ava,oil_date=date1)
        '''
        self.render('yewei.html')

    def post(self):
        oil_h1 = float(self.get_argument('oil_h1', '1'))
        oil_h2 = float(self.get_argument('oil_h2', '1'))
        oil_sum = self.calu_oil_L(oil_h1)+self.calu_oil_L(oil_h2)
        oil_sum_ava = oil_sum-0.7
        '''
        # 总容量30.989
        oil_h1_p = oil_h1/30.989
        oil_h2_p = oil_h2/30.989
        oil_sum_p = oil_sum/(30.989*2)
        '''
        # 
        import time
        # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        date1 = time.strftime("%Y-%m-%d", time.localtime())
        # 插数据
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
        cursor = conn.cursor()
        temp1 = "INSERT INTO oil_high (date,oil_h1,oil_h2,oil_sum,oil_sum_ava) VALUES('%s','%s','%s','%s','%s')"%(date1,oil_h1,oil_h2,oil_sum,oil_sum_ava)
        cursor.execute(temp1)
        temp_sql_result1 = cursor.fetchall()
        # boom_date = (((temp_sql_result1))[0])
        # boom_car_scale = (((temp_sql_result1))[-1])
        conn.commit()
        cursor.close()
        conn.close()

        self.render('yewei1.html', oil_h1=oil_h1,oil_h2=oil_h2,oil_sum=oil_sum,oil_sum_ava=oil_sum_ava,oil_date=date1)




settings = {
    'template_path':os.path.join(os.path.dirname(__file__),"template"),
    'static_path':os.path.join(os.path.dirname(__file__),"static"),
#是/不是\,不然会报错OSError: [Errno 22] Invalid argument
}
current_path = os.path.dirname(__file__)
application = tornado.web.Application([
    (r"/index", SelectHandler),
    (r"/execlupload", dluHandler),
    (r"/dlu", dluHandler),
    (r"/yewei", CalcuHandler),
    
    # (r"/(.*)",StaticFileHandler,{"path":os.path.join(current_path,"template/assets")}),
    # ,"default_filename":"index.html"}),
],**settings)


if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()