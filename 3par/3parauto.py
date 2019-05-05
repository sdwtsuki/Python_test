# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Date: 2017/2/24
# Modified: 2017/3/15
# Author: David Meng
# Script name: auto.py
# Description: main program

import sys
import os
import codecs
import json
from logger import mylogger
from logger import fn_timer_logger
from service import Service
import getpass


def get_args():
    arg_length = sys.argv.__len__()
    system, operation, service1, service2 = "", "", "", ""

    if arg_length not in (3, 4, 5):
        print_usage()
        exit(1)
    elif arg_length == 3:
        # qs start | stop | check | list
        system = sys.argv[1]
        operation = sys.argv[2]
        if system not in ("qs", "ndp", "ib", "zf", "zh", "hg", "ra", "sambank", "wailian", "3par") or operation not in (
                "start", "stop", "check", "list"):
            print_usage()
            exit(1)
    elif arg_length == 4:
        # qs start | stop | check  service1
        system = sys.argv[1]
        operation = sys.argv[2]
        service1 = sys.argv[3]
        if system not in ("qs", "ndp", "ib", "zf", "zh", "hg", "ra", "sambank", "wailian", "3par") or operation not in (
                "start", "stop", "check"):
            print_usage()
            exit(1)
        if not get_srv_ids(system).__contains__(service1):
            print_usage()
            exit(1)
    elif arg_length == 5:
        # qs start | stop | check  service1 service2
        system = sys.argv[1]
        operation = sys.argv[2]
        service1 = sys.argv[3]
        service2 = sys.argv[4]
        if system not in ("qs", "ndp", "ib", "zf", "zh", "hg", "ra", "sambank", "wailian", "3par") or operation not in (
                "start", "stop", "check"):
            print_usage()
            exit(1)
        idlist = get_srv_ids(system)
        if not idlist.__contains__(service1) or not idlist.__contains__(service2):
            print_usage()
            exit(1)
        if idlist.index(service1) > idlist.index(service2):
            print_usage()
            mylogger.error("PARAMETER ERROR: service2 should be after service1 !!!")
            exit(1)
    return system, operation, service1, service2


def print_usage():
    command = ""
    for arg in sys.argv:
        command = command + " " + arg
    mylogger.error("PARAMETER ERROR: %s " % command)
    mylogger.error("COMMAND FORMAT: python auto.py [system] [operation] [service1] [service2]")
    mylogger.error("                -- system:    qs | sambank | ib | ndp | zf | zh | hg | ra | wailian ")
    mylogger.error("                -- operation: start | stop | check | list")
    mylogger.error("                -- service1/service2: Get serviceid using 'list' argument")


def get_separator(command, flag):
    string1 = "#####>>>                                 "
    string2 = "                <<<#####"
    new_string = ""
    if flag == "begin":
        new_string = string1 + "[Begin] " + command + string2
    elif flag == "end":
        new_string = string1 + "[Ended] " + command + string2
    elif flag == "line":
        new_string = "#" * 108
    return new_string


def get_json(system):
    try:
        json_name = system + "_workflow.json"
        if os.path.exists(json_name):
            f = codecs.open(json_name, mode='r', encoding='utf-8')
            service_list = json.load(f)
            f.close()
            return service_list
        else:
            mylogger.error("Json file not found.")
            exit(1)
    except Exception as exp:
        mylogger.error(exp)
        exit(1)


def get_srv_ids(system):
    try:
        json_name = system + "_workflow.json"
        if os.path.exists(json_name):
            f = codecs.open(json_name, mode='r', encoding='utf-8')
            service_list = json.load(f)
            f.close()
            srvids = []
            for service in service_list:
                srvids.append(service["srvid"])
            return srvids
        else:
            mylogger.error("Json file not found.")
            exit(1)
    except Exception as exp:
        mylogger.error(exp)
        exit(1)


@fn_timer_logger
def dostart(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status):
    service = Service(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status)

    if service.start_service():
        mylogger.info("[------------ %s start [success]. Going to next service >>>>>>>>>>]" % service.__str__())
        return True
    else:
        mylogger.error("[------------ %s start [failed]. Workflow terminated! XXXXXXXXXX]" % service.__str__())
        return False


@fn_timer_logger
def dostop(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status):
    service = Service(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status)
    if service.stop == "":
        mylogger.info("[------------ %s stop is NULL.Going to next service >>>>>>>>>>]" % service.__str__())
        return True

    if service.stop_service():
        mylogger.info("[------------ %s stop [success].Going to next service >>>>>>>>>>" % service.__str__())
        return True
    else:
        mylogger.error("[------------ %s stop [failed].Workflow terminated! XXXXXXXXXX]" % service.__str__())
        return False


def docheck(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status):
    service = Service(srvid, ip, username, password, nohupstart, start, nohupstop, stop, needcheck, check, status)

    mylogger.info("-" * 105)
    mylogger.info(":[[ -" + service.check_service1() + "- ]]  : " + service.__str__() + "")
    mylogger.info("-" * 105)


@fn_timer_logger
def main():
    # program run only by devops
    if getpass.getuser() != "devops":
        mylogger.error("This program should only be run by devops!")
        exit(99)

    command = ""
    for arg in sys.argv:
        command = command + " " + arg
    mylogger.info(get_separator(command, "line"))
    mylogger.info(get_separator(command, "begin"))
    mylogger.info(get_separator(command, "line"))

    try:
        system, operation, service1, service2 = get_args()
        service_list = get_json(system)

        if service1 == "" and service2 == "":
            if operation == "start":
                for service in service_list:
                    if dostart(**service):
                        pass
                    else:
                        break
            elif operation == "stop":
                service_list.reverse()
                for service in service_list:
                    if dostop(**service):
                        pass
                    else:
                        break
            elif operation == "check":
                for service in service_list:
                    docheck(**service)
            elif operation == "list":
                for service in service_list:
                    mylogger.info("[ " + service["srvid"] + " ]" + ": " + service["start"])
        elif service2 == "":
            # start one service by id
            if operation == "start":
                for service in service_list:
                    if service["srvid"] == service1:
                        dostart(**service)
            elif operation == "stop":
                for service in service_list:
                    if service["srvid"] == service1:
                        dostop(**service)
            elif operation == "check":
                for service in service_list:
                    if service["srvid"] == service1:
                        docheck(**service)
        else:
            idlist = get_srv_ids(system)
            i = idlist.index(service1)
            j = idlist.index(service2) + 1
            service_list1 = service_list.__getslice__(i, j)
            if operation == "start":
                for service in service_list1:
                    if dostart(**service):
                        pass
                    else:
                        break
            elif operation == "stop":
                service_list1.reverse()
                for service in service_list1:
                    if dostop(**service):
                        pass
                    else:
                        break
            elif operation == "check":
                for service in service_list1:
                    docheck(**service)

    finally:
        mylogger.info(get_separator(command, "line"))
        mylogger.info(get_separator(command, "end"))
        mylogger.info(get_separator(command, "line"))


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print e