import re
import xlrd
import xlwt
from xlutils.copy import copy
import pandas as pd


rvtool_path = r'D:\Documents\Working space\Statistics\20180910\vcent01.xls'
basetable_path = r'D:\Documents\Sundry\python_excel.xls'
vmpurpose_path = r'D:\Documents\Working space\Statistics\20180910\生产环境基线表初稿-20180309.xlsx'
#rvtool_path = input('请输入’RVtool表路径‘及名称：')
#basetable_path = input('请输入’输出基线表‘路径及名称：')

# D:\Documents\Sundry\heh.xls
# D:\Documents\Working space\Statistics\20180910\sxvent.xls
# D:\Documents\Sundry\exceltest.xlsx
data = []
def read_excel():
    workbook = xlrd.open_workbook(rvtool_path)
    sheet_tabvInfo = workbook.sheet_by_name('tabvInfo')
    sheet_tabvNetwork = workbook.sheet_by_name('tabvNetwork')
    sheet_tabvHost = workbook.sheet_by_name('tabvHost')
    workbook2 = xlrd.open_workbook(vmpurpose_path)
    sheet_vmpurpose = workbook2.sheet_by_name('生产环境VM虚机汇总表')


    tabvInfo_VM_num = 0
    tabvInfo_CPUs_num = 0
    tabvInfo_Memory_num = 0
    tabvInfo_Host_num = 0
    tabvInfo_Datacenter_num = 0
    tabvInfo_Cluster_num = 0
    for ii in range(0,sheet_tabvInfo.ncols):        #tabvInfo取到需要取的列的excel列号
        if sheet_tabvInfo.cell(0,ii).value=='VM':
            tabvInfo_VM_num = ii
        elif sheet_tabvInfo.cell(0,ii).value=='CPUs':
            tabvInfo_CPUs_num = ii
        elif sheet_tabvInfo.cell(0,ii).value=='Memory':
            tabvInfo_Memory_num = ii
        elif sheet_tabvInfo.cell(0,ii).value=='Host':
            tabvInfo_Host_num = ii
        elif sheet_tabvInfo.cell(0,ii).value=='Datacenter':
            tabvInfo_Datacenter_num = ii
        elif sheet_tabvInfo.cell(0,ii).value=='Cluster':
            tabvInfo_Cluster_num = ii

    tabvHost_CPU_num = 0
    tabvHost_Core_num = 0
    tabvHost_Memory_num = 0
    tabvHost_Active_num = 0
    tabvHost_Model_num = 0
    tabvHost_tag_num = 0
    for ii in range(0,sheet_tabvHost.ncols):        #tabvHost取到需要取的列的excel列号
        if sheet_tabvHost.cell(0,ii).value=='HT Active':
            tabvHost_Active_num = ii
        elif sheet_tabvHost.cell(0,ii).value=='# CPU':
            tabvHost_CPU_num = ii
        elif sheet_tabvHost.cell(0,ii).value=='# Cores':
            tabvHost_Core_num = ii
        elif sheet_tabvHost.cell(0,ii).value=='# Memory':
            tabvHost_Memory_num = ii
        elif sheet_tabvHost.cell(0,ii).value=='Model':
            tabvHost_Model_num = ii
        elif sheet_tabvHost.cell(0,ii).value=='Service tag':
            tabvHost_tag_num = ii

    tabvNetwork_IP_num = 0
    for ii in range(0,sheet_tabvNetwork.ncols):        #tabvInfo取到需要取的列的excel列号
        if sheet_tabvNetwork.cell(0,ii).value=='IP Address':
            tabvNetwork_IP_num = ii


    i=1
    for i in range(0,sheet_tabvInfo.nrows-1):
        arr = []
        rows = sheet_tabvInfo.row_values(i+1)    # 获取tabvInfo第i+1行内容(不获取第一行)
        j=1
        ipstr = ['','','','']
        for j in range(0,sheet_tabvNetwork.nrows-1):        #获取某行4种ip地址功能
            netrows = sheet_tabvNetwork.row_values(j+1)    # 获取第i+1行内容(不获取第一行)
            if netrows[0] == rows[tabvInfo_VM_num]:
                if re.search(r'((1\d{2}|25[0-5]|2[0-4]\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)',netrows[tabvNetwork_IP_num]) != None:  #选取出ip地址
                    ip = re.search(r'((1\d{2}|25[0-5]|2[0-4]\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)',netrows[tabvNetwork_IP_num]).group()

                    if re.search('^10\.254\..*?',ip) == None and re.search('^10\.252\..*?',ip) == None :            #在此处设置业务地址，管理地址，备份地址，nas地址规则
                        ipstr[0]=ip
                    elif re.search('^10\.254\..*?3\..*?',ip) != None :
                        ipstr[2] = ip
                    elif re.search('^10\.254\..*?1\..*?',ip) != None :
                        ipstr[3] = ip
                    else:
                        ipstr[1] = ip


        h=1
        hoststr = []
        for h in range(0,sheet_tabvHost.nrows-1):        #获取主机相关信息，4种
            hostrows = sheet_tabvHost.row_values(h+1)

            if hostrows[0] == rows[tabvInfo_Host_num]:
                hoststr.append(hostrows[tabvHost_Model_num])
                hoststr.append(hostrows[tabvHost_tag_num])
                if hostrows[tabvHost_Active_num]== 'True':
                    hoststr.append( int(hostrows[tabvHost_CPU_num])*int(hostrows[tabvHost_Core_num]) )
                else:
                    hoststr.append(int(hostrows[tabvHost_Core_num]))

                hoststr.append(int(hostrows[tabvHost_Memory_num] / 1000))  # 取内存（需要改）


        #从基线表里获取vm的用途（‘应用系统’列）根据实际情况，注销该循环
        # k = 1
        # vmpurposestr = ['']
        # for k in range(0, sheet_vmpurpose.nrows - 1):  # 获基线表初稿
        #     vmpurposerows = sheet_vmpurpose.row_values(k + 1)
        #     if rows[tabvInfo_VM_num] == vmpurposerows[11]:
        #         vmpurposestr[0] = vmpurposerows[10]


        arr.append(rows[tabvInfo_Datacenter_num])   #将datacent列加入第一列
        arr.append(rows[tabvInfo_Cluster_num])   #将cluster列加入第二列
        arr.append(rows[tabvInfo_Host_num])   #将host列加入第三列
        arr.append(hoststr[0])    #host型号
        arr.append(hoststr[1])    #host序列号
        arr.append(hoststr[2])      #超线程
        arr.append('')
        arr.append('')
        arr.append(hoststr[3])      #host总内存
        arr.append('')
        arr.append('')
        arr.append('')       #应用系统列
        arr.append(rows[tabvInfo_VM_num])    #vm名称
        arr.append(ipstr[0])
        arr.append(ipstr[1])
        arr.append(ipstr[2])
        arr.append(ipstr[3])
        arr.append(int(rows[tabvInfo_CPUs_num]))    #虚拟cpu
        arr.append(int(rows[tabvInfo_Memory_num]/1000))
        data.append(arr)
    return data


def write_excel():

    read_excel()

    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    row0 = [u'数据中心', u'集群', u'ESXI主机',u'主机型号',u'主机序列号',u'超线程', u'已用VCPU', u'可用cpu', u'总内存', u'已用内存', u'可用内存', u'应用系统\
', u'VM', u'业务地址', u'管理地址', u'应用备份', u'NAS地址', u'虚机CPU', u'虚机内存']

    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i])

    for j in range(0,len(data)):
        data_row = data[j]
        for h in range(0,len(data_row)):
            sheet1.write(j+1,h,data_row[h])



    workbook.save(basetable_path)


def pandas_excel():

    write_excel()

    data = pd.DataFrame(pd.read_excel(basetable_path))
    data1 = data.sort_values(by=['数据中心','集群','ESXI主机'])    #按前三列排序
    data1.to_excel(basetable_path,sheet_name='VM基线表')

    # rb = xlrd.open_workbook(basetable_path, formatting_info=True)
    # #rs = rb.sheet_by_name('VM基线表')
    # wb = copy(rb)
    # ws = wb.get_sheet(0)
    # ws.write_merge(1, 4, 4, 4)
    # wb.save(basetable_path)


def merge_excel():

    pandas_excel()

    col_name_datacenter = '数据中心'
    col_name_esxi = 'ESXI主机'
    col_name_cluster = '集群'
    workbook = xlrd.open_workbook(basetable_path)
    sheet_xlrd = workbook.sheet_by_name('VM基线表')

    def get_tomerge_col_num(col_name):  # 获取需要合并列的列号
        for i in range(0, sheet_xlrd.row_len(0)):
            if sheet_xlrd.cell_value(0, i) == col_name:
                return i

    col_num_datacenter = get_tomerge_col_num(col_name_datacenter)
    col_num_cluster = get_tomerge_col_num(col_name_cluster)
    col_num_esxi = get_tomerge_col_num(col_name_esxi)

    startnum = 0
    stopnum = 0
    merge_num_arr = []
    def get_tomerge_cell(col_num, startnum=0, stopnum=0):  # 获取需要合并的cell的行号
        j = 1
        for j in range(1, sheet_xlrd.nrows + 1):
            if j + 1 < sheet_xlrd.nrows:
                if sheet_xlrd.cell_value(j, col_num) == sheet_xlrd.cell_value(j + 1, col_num):
                    stopnum += 1

                else:
                    merge_num_arr.append(
                        [startnum + 1, stopnum + 1, col_num, sheet_xlrd.cell_value(startnum + 1, col_num)])
                    stopnum += 1
                    startnum = stopnum

        return merge_num_arr

    esxi = get_tomerge_cell(col_num_esxi)
    esxi_mergecows = []
    for y in esxi:
        esxi_mergecows.append([y[0], y[1]])

    get_tomerge_cell(col_num_cluster)
    get_tomerge_cell(col_num_datacenter)

    rb = xlrd.open_workbook(basetable_path, formatting_info=True)
    # rs = rb.sheet_by_name('VM基线表')
    wb = copy(rb)
    ws = wb.get_sheet(0)
    for x in merge_num_arr:  # 前三列根据各自的相同内容合并
        ws.write_merge(x[0], x[1], x[2], x[2], x[3])

    arr = ['主机型号', '主机序列号', '超线程', '已用VCPU', '可用cpu', '总内存', '已用内存', '可用内存']
    esxi_arr = []
    for yy in arr:
        esxi_arr.append(get_tomerge_col_num(yy))

    col_name_vmcpu = '虚机CPU'
    col_name_vmmemory = '虚机内存'
    col_num_vmcpu = get_tomerge_col_num(col_name_vmcpu)
    col_num_vmmemory = get_tomerge_col_num(col_name_vmmemory)

    for xx in esxi_mergecows:
        for xxx in esxi_arr:    # 根据esxi来合并
            ws.write_merge(xx[0], xx[1], xxx, xxx, sheet_xlrd.cell_value(xx[0], xxx))   #这里的xx[0]和xx[1]即为每个esxi合并的开始和结束的行号

        vmcpu_sum = 0
        for m in range(xx[0],xx[1]+1):
            vmcpu_sum +=int(sheet_xlrd.cell_value(m, col_num_vmcpu))

        ws.write(xx[0],esxi_arr[3],vmcpu_sum)    #写入'已用VCPU'的值
        vmmemory_sum = 0
        for n in range(xx[0], xx[1]+1):
            vmmemory_sum +=int(sheet_xlrd.cell_value(n, col_num_vmmemory))

        ws.write(xx[0], esxi_arr[6], vmmemory_sum)  # 写入'已用内存'的值

        #ws.write(xx[0], esxi_arr[4], int(sheet_xlrd.cell_value(xx[0], esxi_arr[2]))-int(sheet_xlrd.cell_value(xx[0], esxi_arr[3])) )    # 写入'可用cpu'的值
        #ws.write(xx[0], esxi_arr[7], int(sheet_xlrd.cell_value(xx[0], esxi_arr[5])) - int(sheet_xlrd.cell_value(xx[0], esxi_arr[6])))   # 写入'可用内存'的值

    wb.save(basetable_path)
    print('程序执行完毕！')


merge_excel()
