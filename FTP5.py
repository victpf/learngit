#coding:utf-8
from ftplib1 import FTP
import re,os,time,datetime,string,sys
import socket
# 这个版本支持输入多个suffix，程序会遍历并且选择prefix.**.suffix的dataset，然后下载里边的内容
class MYFTP:
    def __init__(self, hostname, port, username, password,local_dir,remote_dir,ds_filter):
        self.hostname=hostname
        self.port = port
        self.username=username
        self.password=password
        self.remote_dir = remote_dir
        self.local_dir = local_dir
        self.ftp = FTP()
        self.dslist=[]
        self.filelist=[]
        self.ds_filter=ds_filter
    def __del__(self):
        self.ftp.close()
    def connftp(self):
        ftp = self.ftp
        try:
            timeout = 30
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)  
            print(timeout)
            print('开始连接到 %s'%(self.hostname))
            ftp.connect(self.hostname,self.port)
            print('成功连接到 %s'%(self.hostname))
            print('开始登录到 %s'%(self.hostname))
            ftp.login(self.username,self.password)
            print('成功登录到 %s'%(self.hostname))
        except Exception:
            deal_error('连接或登录失败')

    def get_dataset_list(self,listl):
        self.dslist=[]
        for i in range(len(listl)):
            alist = listl[i].split(' ')         
            for k in range(len(self.ds_filter)):
                if self.ds_filter[k] in alist[-1]:
                    self.dslist.append(alist[-1])
                else:
                    pass
            print('SELF_DSLIST IS NOW: %s'%self.dslist)
    def get_file_list(self,listl):
        self.filelist=[]
        for i in range(len(listl)):
            alist = listl[i].split(' ')
            if not '' == alist[0]:
                self.filelist.append(alist[0])
            else:
                pass
    def download_file(self, localfile,remotefile):
        file_handle = open(localfile,'wb')
        self.ftp.retrascii('RETR %s'%(remotefile),file_handle.write)
        file_handle.close()
    def download_files(self,local_dir='./',remote_dir='./'):
        print('Local Dir is now: %s'%local_dir)
#        remote_dir=self.remote_dir
        self.ftp.cwd('..')
        self.ftp.cwd(remote_dir)
        print(self.ftp.pwd())
#        self.ftp.cwd('TPF')
        list0 = []
        self.ftp.dir(list0.append)
#        print(list0)
        self.get_dataset_list(list0)
        for i in range(len(self.dslist)):
            self.ftp.cwd(self.dslist[i])
            print(self.ftp.pwd())
            list1 = []
            self.ftp.dir(list1.append)
#            print(list1)
            self.get_file_list(list1)
            print(self.filelist)
            local = os.path.join(self.local_dir,self.remote_dir+'.'+self.dslist[i])
            print('local is now: %s'%local)
#            local_file_list = os.listdir(local)
            
            if not os.path.exists(local):
                os.makedirs(local)
            local_file_list = os.listdir(local)
            print('Local_file_list is now: %s'%local_file_list)
#			判断文件是不是已经下载过，如果是，那么直接pass，如果不是,则启动新的下载			
            for j in range(len(self.filelist)):
#                info = os.getcwd()
                if self.filelist[j] in local_file_list:
                    pass
                else:
                    self.download_file(local+'\\'+self.filelist[j],self.filelist[j])
#                   self.download_file(local+'\\'+self.filelist[j]+'.txt',self.filelist[j])
#            self.ftp.cwd('/')  将会使目录切换到USS的根目录
            for k in range(len(self.ftp.pwd().split('.'))):
                self.ftp.cwd('..')
            self.ftp.cwd(remote_dir)
            local = ''              

def deal_error(e):  
    timenow  = time.localtime()  
    datenow  = time.strftime('%Y-%m-%d', timenow)  
    logstr = '%s 发生错误: %s' %(datenow, e)  
    debug_print(logstr)  
#    file.write(logstr)  
    sys.exit() 

def debug_print(s):  
    print (s)

    
if __name__ == '__main__':
#    file = open('C:\tpf\log.txt','a')
    hostname= input('Pls input HOST IP: ')
    username='ROOT'
    password='TIVMVS'
    remote_dir = 'TPF'
    local_dir1=input('Pls input Local dir to store the downloaded file: ')
    print(local_dir1)
    if not os.path.exists(local_dir1 + '\\\\' + hostname):
        os.makedirs(local_dir1 + '\\\\' + hostname)
    local_dir = os.path.join(local_dir1, hostname)
    print('Local Dir: %s'%local_dir)
    port = 21
    ds_filter = []
    s = input('Pls input the suffix: ')
    print(s)
    while(s != ''):
        ds_filter.append(s)
        s = input('Pls input the suffix: ')
    print('ds_filter is now: %s'%ds_filter)
#    print('remote_dir is now: %s'%remote_dir)
    f = MYFTP(hostname, 21, 'ROOT', 'WI0NW5GF',local_dir,'TPF',ds_filter)
    f.connftp()
    f.download_files(local_dir,remote_dir)
