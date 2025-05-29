namespace py log_event
namespace java com.streamflow.logging

struct LogMetaData {
    1: optional string request_id
    2: optional string ip_address
    3: optional string http_method
    4: optional string endpoint
}


struct logEvent {
    1: required i64 timestamp           // Unix epoch millis
    2: required string service_name     // auth-service, payment-service,etc..
    3: required string log_level        // INFO, DEBUG, ERROR, etc..
    4: required string message
    5: optional string environment
    6: optional string user_id
    7: optional LogMetaData metadata 
}

service LogIngestionService {
    void sendLog(1: LogEvent log)
}
