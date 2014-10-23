__author__ = 'ict'

import socket
import os

import DAL.file
import service.configure
import service.object_pool
from service.helper import package
from service.helper import response
from service.file import send_file
from service.file import receive_file


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect((self.ip, self.port))
        msg = self.sk.recv(256).decode()
        if msg != "start":
            raise Exception("Can not connect")

    def close(self):
        self.sk.send(package("close"))
        self.sk.close()

    def save(self, var, name):
        self.sk.send(package("save"))
        data_type = str(type(var))[8:-2]
        filename = name + "." + data_type
        DAL.file.save(var, filename)
        response(self.sk, "name", name)
        response(self.sk, "type", data_type)
        state = self.sk.recv(service.configure.msg_buffer).decode()
        if state != service.object_pool.success_msg:
            return state
        send_file(self.sk, filename)
        os.remove(filename)
        return state

    def load(self, name):
        self.sk.send(package("load"))
        response(self.sk, "name", name)
        filename = self.sk.recv(service.configure.msg_buffer).decode()
        if filename == service.configure.no_such_object:
            return None
        state = self.sk.recv(service.configure.msg_buffer).decode()
        if state != service.object_pool.success_msg:
            return None
        receive_file(self.sk, filename)
        var = DAL.file.load(filename)
        os.remove(filename)
        return var

    def remove(self, name):
        self.sk.send(package("remove"))
        response(self.sk, "name", name)
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        if rst == service.object_pool.success_msg:
            return name + " has been removed"
        else:
            return rst

    def list(self):
        self.sk.send(package("list"))
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        return eval(rst)

    def rename(self, src_name, dst_name):
        self.sk.send(package("rename"))
        response(self.sk, "name", src_name)
        response(self.sk, "rename", dst_name)
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        return rst

    def clone(self, src_name, dst_name):
        self.sk.send(package("clone"))
        response(self.sk, "name", src_name)
        response(self.sk, "clonename", dst_name)
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        return rst

    def compute_feature(self, src_name, dst_name, mtd, option, main, unpack=False):
        self.sk.send(package("feature"))
        response(self.sk, "name", src_name)
        response(self.sk, "rstname", dst_name)
        response(self.sk, "mtd", str(mtd))
        response(self.sk, "option", str(option))
        response(self.sk, "main", str(main))
        response(self.sk, "unpack", str(unpack))
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        return rst

    def compute_pca(self, src_name, dst_name, n=0):
        self.sk.send(package("pca"))
        response(self.sk, "name", src_name)
        response(self.sk, "rstname", dst_name)
        response(self.sk, "n", str(n))
        rst = self.sk.recv(service.configure.msg_buffer).decode()
        return rst