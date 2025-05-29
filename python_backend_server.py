# server.py
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from gen_py.log_event import LogEventService
from gen_py.log_event.ttypes import LogEvent

class LogEventHandler:
    def sendLog(self, log):
        print(f"[{log.timestamp}] {log.level} - {log.message} (Service: {log.service})")
        if log.metadata:
            print(f"Metadata: {log.metadata}")
        print("-" * 40)

if __name__ == "__main__":
    handler = LogEventHandler()
    processor = LogEventService.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Starting the log receiver server...")
    server.serve()
