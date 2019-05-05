# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Date: 2017/2/24
# Modified: 2017/3/9 18:50
# Author: David Meng
# Script name: service.py
# Description: service class definition

import paramiko
from logger import fn_timer_logger
from logger import mylogger
import time


class Service():
    def __init__(self, srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status):

        # Service class definition
        # Attributes:
        # nohupstart:   YES/NO
        # nohupstart:   YES/NO
        # status:       STARTED/STOPPED
        # start, stop, check:
        # Script or command to do start/stop/check which stored on destination hosts.
        # needcheck:    Signal of if check needed

        self.srvid = srvid
        self.ip = ip
        self.username = username
        self.password = password
        self.nohupstart = nohupstart
        self.start = start
        self.nohupstop = nohupstop
        self.stop = stop
        self.needcheck = needcheck
        self.check = check
        self.status = status

    def __str__(self):
        """
            :return a string which represent service object
        """
        return "%s@%s" % (self.srvid, self.ip)

    def conn(self):
        """ Create ssh connection.
            启动服务.
        Create ssh connection using parameters given to service instance,using module paramiko.
        使用paramiko模块，通过service实例给定参数建立ssh连接。
        Args:
        参数：
            ip,username,password
            指定ssh超时时间timeout 5s
        Returns:
        返回值：
            Return a ssh connection .
            返回一个ssh连接。
        Raises:
            exceptions
            发生异常时时记录异常信息
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.username, password=self.password, timeout=5)
            mylogger.debug("Connected to %s." % self.ip)
            return ssh
        except Exception as exceptions:
            mylogger.error(exceptions)

    def release(self, ssh):
        """ Disconnect a ssh connection.
            释放连接.
        Release a ssh connection using close()
        释放ssh连接
        Args:
        参数：
            sshclient
        Returns:
            no return values
        Raises:
            exceptions
            发生异常时时记录异常信息
        """
        try:
            ssh.close()
            mylogger.debug("Disconnected from %s." % self.ip)
        except Exception as exceptions:
            mylogger.error(exceptions)
        finally:
            ssh.close()

    def get_separator(self, name):
        string = "----------------------"
        new_string = ""
        if name == "begin":
            new_string = string + "[Begin] " + self.__str__() + string
        elif name == "end":
            new_string = string + "[Ended] " + self.__str__() + string
        return new_string

    @fn_timer_logger
    def start_service(self):
        """ start service .
            启动服务.
        Start service by running scripts like db2start.sh on server.
        通过执行服务器上的启动脚本，如db2start.sh，启动服务。
        Args:
        参数：
            sshclient, nohupstart, start
            ssh连接，是否为nohup启动方式:YES/NO，启动脚本:/path/startscript.sh
        Returns:
        返回值：
            Return boolean values.True while service start successfully,False while not.
            返回布尔类型值：True代表服务启动成功，False反之。
        Raises:
            exceptions
            发生异常时时记录异常信息，返回False
        """
        try:
            mylogger.debug(self.get_separator("begin"))
            sshclient = self.conn()
            command = self.start

            if self.nohupstart == "YES":
                mylogger.info("NOHUP Starting %s ..." % self.__str__())
                mylogger.debug(command)
                channel = sshclient.get_transport().open_session()
                mylogger.debug(command)
                channel.exec_command(command)
                if self.needcheck == "YES":
                    for i in range(15):
                        if self.check_service(sshclient):
                            mylogger.info("NOHUP start %s [SUCCESS]!" % self.__str__())
                            self.status = "STARTED"
                            self.release(sshclient)
                            return True
                        time.sleep(1)
                    # if for loop ended without return ,means check failed.
                    mylogger.info("NOHUP start %s [FAILED]!" % self.__str__())
                    self.release(sshclient)
                    return False
                else:
                    mylogger.info("Check is NO, service started success by default.")
                    mylogger.info("NOHUP start%s [SUCCESS]!" % self.__str__())
                    self.status = "STARTED"
                    self.release(sshclient)
                    return True
            else:
                """
                    Common way startup:
                        simulate a shell, execute command, and exit shell return to python program
                """
                mylogger.info("Common Starting %s ..." % self.__str__())
                mylogger.debug(command)

                srvid = self.srvid

                if srvid.__contains__("DB2"):
                    stdin, stdout, stderr = sshclient.exec_command(command)
                    output = stdout.read()
                    errs = stderr.read()
                else:
                    channel = sshclient.invoke_shell()
                    # 如果shell在200s秒内无任何输出，则会中断
                    channel.settimeout(200)
                    stdin = channel.makefile('wb')
                    stdout = channel.makefile('rb')
                    stderr = channel.makefile_stderr('rb')
                    if self.srvid == "QS-CMSA-union":
                        stdin.write('''
                        \n
                        %s
                        y
                        exit
                        ''' % command)
                    else:
                        stdin.write('''
                        %s
                        exit
                        ''' % command)

                    output = ""
                    errs = ""
                    try:
                        output = stdout.read()
                        errs = stderr.read()
                    except Exception, e:
                        mylogger.error(e)

                if len(output) > 0:
                    mylogger.info(output)
                if len(errs) > 0:
                    mylogger.error(errs)
                if self.needcheck == "YES":
                    for i in range(15):
                        if self.check_service(sshclient):
                            mylogger.info("NOHUP start %s [SUCCESS]!" % self.__str__())
                            self.status = "STARTED"
                            self.release(sshclient)
                            return True
                        time.sleep(1)
                else:
                    mylogger.info("Check is passed, service start considered success.")
                    mylogger.info("Common start %s [SUCCESS]..." % self.__str__())
                    self.status = "STARTED"
                    self.release(sshclient)
                    return True
        except Exception as e:
            mylogger.error(e)
            return False
        finally:
            mylogger.debug(self.get_separator("end"))

    @fn_timer_logger
    def stop_service(self):
        """ stop service .
            停止服务.
        Stop service by running scripts like db2stop.sh on server.
        通过执行服务器上的服务检查脚本，如db2stop.sh，停止服务。
        Args:
        参数：
            sshclient, nohupstop, stop
        Returns:
        返回值：
            Return boolean values.True while service stop successfully,False while not.
            返回布尔类型值：True代表服务停止成功，False反之。
        Raises:
            exceptions
            发生异常时时记录异常信息
        """
        try:
            command = self.stop
            if command == "":
                mylogger.info("Check is NULL! service stop considered success.")
                mylogger.info("Stop %s [SUCCESS]!" % self.__str__())
                self.status = "STOPPED"
                return True

            mylogger.debug(self.get_separator("begin"))
            sshclient = self.conn()

            mylogger.info("Stopping %s ..." % self.__str__())
            mylogger.debug(command)
            channel = sshclient.invoke_shell()
            # 如果shell在200s秒内无任何输出，则会中断
            channel.settimeout(200)
            stdin = channel.makefile('wb')
            stdout = channel.makefile('rb')
            stderr = channel.makefile_stderr('rb')
            if self.srvid == "QS-CMSA-union":
                stdin.write('''
                \n
                %s
                y
                exit
                ''' % command)
            else:
                stdin.write('''
                %s
                exit
                ''' % command)
            output, errs = "", ""
            try:
                output = stdout.read()
                errs = stderr.read()
            except Exception, e:
                mylogger.error(e)

            mylogger.info(output)
            mylogger.error(errs)
            # 默认认为停服务成功
            mylogger.info("Check is passed for stop, service stop considered success.")
            mylogger.info("Stop %s [SUCCESS]!" % self.__str__())
            self.status = "STOPPED"
            self.release(sshclient)
            return True
        except Exception as e:
            mylogger.error(e)
        finally:
            mylogger.debug(self.get_separator("end"))

    @fn_timer_logger
    def check_service(self, sshclient):
        """ Check service status.
            使用传入连接，检查服务状态，以解决重复创建连接问题.
        Checking service status by running scripts like db2check.sh on server.
        通过执行服务器上的服务检查脚本，如db2check.sh，确定服务是否活动。
        Args:
        参数：
            check,status
            检查脚本，状态
        Returns:
        返回值：
            Return boolean values.True while service running,False while not.
            返回布尔类型值：True代表服务已启动，False反之。
        Raises:
            exceptions
            发生异常时时记录异常信息，返回False
        """
        try:
            command = self.check

            if command == "":
                mylogger.error("CHECK ERROR:check command is null.")
                return False

            stdin, stdout, stderr = sshclient.exec_command(command)
            output = stdout.read()
            errs = stderr.read()
            mylogger.debug(command)
            mylogger.info(output)

            # only way to return success is get keyword "_SUCCESS_"
            if len(output) > 0:
                if output.__contains__("_SUCCESS_"):
                    mylogger.info("CHECK  %s [SUCCESS]!" % self.__str__())
                    return True
                else:
                    mylogger.info("CHECK  %s [FAILED]!" % self.__str__())
                    return False
            if len(errs) > 0:
                mylogger.error("CHECK ERROR:command error happened.")
                mylogger.error(errs)
            return False
        except Exception as e:
            mylogger.error(e)

    def check_service1(self):
        """ Check service status.
            自行创建连接，检查服务状态
            不记录任何操作日志
            成功返回started，失败返回stopped，检查命令为空返回unknown
        """
        try:
            command = self.check
            # check命令为空，则直接打印信息，返回True，继续流程
            if command == "":
                return "Unknown"

            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.username, password=self.password, timeout=5)
            stdin, stdout, stderr = ssh.exec_command(command)
            try:
                output = stdout.read()
                if len(output) > 0:
                    if output.__contains__("_SUCCESS_"):
                        return "Started"
                    else:
                        return "Stopped"
                else:
                    return "Stopped"
            except Exception, e:
                print e
            ssh.close()
            return "Stopped"
        except Exception as e:
            print e