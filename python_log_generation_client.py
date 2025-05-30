from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from gen_py.log_event import LogIngestionService
from gen_py.log_event.ttypes import logEvent, LogMetaData

from faker import Faker
import random
import time

fake = Faker()

log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
services = ["auth-service", "order-service", "payment-service", "inventory-service"]
endpoints = ["/api/login", "/api/order", "/api/pay", "/api/stock"]
host =["web-01.prod.us-west",
    "api-02.dev.us-east",
    "db-03.stage.eu-central",
    "batch-04.prod.ap-south",
    "analytics-05.qa.us-west",
    "stream-06.dev.us-central",
    "ingest-07.prod.eu-west",
    "cache-08.stage.us-east",
    "proxy-09.prod.ap-northeast",
    "service-10.qa.eu-north"]

def generate_random_log_event():
    metadata = LogMetaData(
        request_id=fake.uuid4(),
        ip_address=fake.ipv4(),
        http_method=random.choice(["GET", "POST", "PUT", "DELETE"]),
        endpoint=random.choice(endpoints)
    )

    log = logEvent(
        timestamp=int(time.time() * 1000),
        service_name=random.choice(services),
        log_level=random.choice(log_levels),
        message=fake.sentence(),
        environment=random.choice(["dev", "qa", "prod"]),
        user_id=f"user-{fake.random_int(min=1000, max=9999)}",
        metadata=metadata
        host = random.choice(host) ## sending the new optional field towards a server which is 
        ## not expecting it. It is NEW CLIENT --> OLD SERVER-- BACKWARD COMPATIBILITY
    )

    return log

def main():
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = LogIngestionService.Client(protocol)
    transport.open()

    # Generate and send 10 synthetic logs
    for i in range(15):
        log = generate_random_log_event()
        print(log)
        client.sendLog(log)
        print(f"✅ Sent log {i+1}: {log.service_name} - {log.log_level}")
        time.sleep(0.5)  # optional: wait a bit to simulate real traffic

    transport.close()

if __name__ == "__main__":
    main()
