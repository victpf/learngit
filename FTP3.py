#coding:utf-8
from ftplib1 import FTP
import re,os,time,datetime,string,sys
import socket

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
        self.ds_filter= ds_filter
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
#'''        try:
#            ftp.cwd('..')
#            ftp.cwd(self.remote_dir)
#        except(Exception):
#            deal_error('设定默认远程目录失败')'''
    def get_dataset_list(self,listl):
        self.dslist=[]
        for i in range(len(listl)):
            alist = listl[i].split(' ')
            if self.ds_filter in alist[-1]:
                self.dslist.append(alist[-1])
            else:
                pass
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
#            print(self.dslist)
#            print('zzzzz: %s'%self.dslist[i])
            self.ftp.cwd(self.dslist[i])
            print(self.ftp.pwd())
            list1 = []
            self.ftp.dir(list1.append)
#            print(list1)
            self.get_file_list(list1)
            print(self.filelist)
            local = os.path.join(self.local_dir,self.remote_dir+'.'+self.dslist[i])
            print('local is now: %s'%local)
            if not os.path.exists(local):
                os.makedirs(local)
            for j in range(len(self.filelist)):
                self.download_file(local+'\\'+self.filelist[j]+'.txt',self.filelist[j])
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
    hostname= input('Pls input host IP: ')
    username=input('Pls input username: ')
    password=input('Pls input passwd: ')
    remote_dir = input('Pls input Dataset Prefix(default is TPF): ')
    local_dir1=input('Pls input Local dir to store the downloaded file: ')
    print(local_dir1)
    if not os.path.exists(local_dir1 + '\\\\' + hostname):
        os.makedirs(local_dir1 + '\\\\' + hostname)
    local_dir = os.path.join(local_dir1, hostname)
    print('Local Dir: %s'%local_dir)
    port = 21
    ds_filter = input('Pls input the dstaset filter/suffix(default is JCL): ')
    print('remote_dir is now: %s'%remote_dir)
    f = MYFTP(hostname, port, username, password,local_dir,remote_dir,ds_filter)
    f.connftp()
    f.download_files(local_dir,remote_dir)
