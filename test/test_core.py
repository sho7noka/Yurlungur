# -*- coding: utf-8 -*-
import sys
import unittest
import rpyc
# conn = rpyc.classic.connect("localhost")

sys.path.append('../yurlungur')

# print(conn.modules.sys)

# from yurlungur.core import application
#
#
# class TestCore(unittest.TestSuite):
#
#     def test_app(self):
#         self.assertTrue(application == "standalone")
#
#     def test_cli(self):
#         import yurlungur
#         print(yurlungur.blender.shell("print(2)"))
#
#
# if __name__ == '__main__':
#     unittest.main()

import time
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

##########################################################################################
class TestSvc(object):
	def ping(self, pid, _sleep=0):
		for i in range(_sleep):
			print ("[%d] %d" % (pid, i))
			time.sleep(1)
		return True

##########################################################################################
def main():

	mgr = TestSvc()
	from socketserver import ThreadingMixIn
	class SimpleThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
		allow_reuse_address = True
	class RequestHandler(SimpleXMLRPCRequestHandler):
		rpc_paths = ('/TestSvc')
	server = SimpleThreadXMLRPCServer(('0.0.0.0', 9012),
			                            requestHandler=RequestHandler,
			                            logRequests=False,
			                            allow_none=True,
	)
	server.register_introspection_functions()
	server.register_instance(mgr)
	server.register_instance(server.shutdown, "close")
	server.serve_forever()

##########################################################################################
if __name__=='__main__':
	main()

import os
import xmlrpc.client as xmlrpclib
proxy = xmlrpclib.ServerProxy("http://localhost:9012/TestSvc")
print ("[%d] TestSvc.ping(5)=%s" % (os.getpid(), proxy.ping(os.getpid(), 5)))


import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor, as_completed
import socket


def submit_sleep():
	server = xmlrpc.client.ServerProxy("http://localhost:8002/", allow_none=False)
	return server.sleep()

with ThreadPoolExecutor() as executor:
	sleeps = {executor.submit(submit_sleep) for _ in range(4)}
	for future in as_completed(sleeps):
		sleep_time = future.result()
		print(sleep_time)
server = xmlrpc.client.ServerProxy("http://localhost:8002/", allow_none=False)
server.close()
import random
import time
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer, MultiPathXMLRPCServer


class SimpleThreadedXMLRPCServer(ThreadingMixIn, MultiPathXMLRPCServer):
    pass


# sleep for random number of seconds
def sleep():
    r = random.randint(2, 10)
    print('sleeping {} seconds'.format(r))
    time.sleep(r)
    return 'slept {} seconds, exiting'.format(r)


# run server
def run_server(host="localhost", port=8000):
    server_addr = (host, port)
    server = SimpleThreadedXMLRPCServer(server_addr)
    server.allow_reuse_address = True
    server.register_function(sleep, 'sleep')
    server.register_function(server.shutdown, "close")

    print("Server thread started. Testing server ...")
    print('listening on {} port {}'.format(host, port))

    server.serve_forever()


if __name__ == '__main__':
    run_server()