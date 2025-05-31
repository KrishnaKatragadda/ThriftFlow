# ThriftFlow
A Cross language Log Ingestion and evolvable Pipeline

# 🔄 Thrift-Based Cross-Language Logging System (Python-only Demo)

This project demonstrates how to build a lightweight and efficient logging system using [Apache Thrift](https://thrift.apache.org/) with:

- ✅ **Schema evolution** (backward and forward compatibility)
- 🧱 **Protocol flexibility** (Binary, JSON, etc.)
- 🐍 **Fully implemented in Python**

---

## 📖 Project Overview

Imagine a microservice architecture where services emit logs in a structured format. To future-proof the system and allow for growth, we use Apache Thrift to define a schema that can evolve over time without breaking downstream consumers.

This project simulates:

- A **Python client** emitting structured log events.
- A **Python server** receiving and storing those logs.
- Evolution of the logging schema with **backward and forward compatibility**.

---

## 📐 Thrift Schema Definition

```thrift
namespace py log_event

struct LogEvent {
  1: i64 timestamp
  2: string service
  3: string host
  4: string message
  // Newly added field
  5: optional string log_level
}

```
---

Field 5 is optional — making it safe to add without breaking older consumers.
This schema is shared between both client and server.

## Project Structure

```
thrift-logging-python/
├── thrift/
│   └── log_event.thrift        # Shared Thrift schema
├── gen-py/
│   └── log_event/              # Thrift-generated Python code
├── server.py                   # Receives and logs events
├── client.py                   # Sends log events
```

🧪 Compatibility Scenarios
✅ Backward Compatibility
New client sends log_level → Old server (without that field) ignores it safely.

✅ Forward Compatibility
Old client sends logs (without log_level) → New server handles it as None.


| Action                | Safe? | Notes                                                               |
| --------------------- | ----- | ------------------------------------------------------------------- |
| Add optional field    | ✅     | Preferred way to evolve schemas                                     |
| Remove a field        | ✅     | Older clients may still send it; ignored safely                     |
| Rename a field        | ✅     | ID and type must remain unchanged                                   |
| Change a field's type | ❌     | Breaks compatibility – Thrift uses field ID and type to deserialize |
| Reuse a field ID      | ❌     | Never reuse IDs; it may break older/newer clients                   |

🌍 Protocol Flexibility
Thrift supports multiple wire protocols. You can choose one based on needs:

TBinaryProtocol – default, fast

TCompactProtocol – more compact

TJSONProtocol – human-readable, good for debugging

Client and server must agree on the protocol used.

🛠️ Setup & Execution
1. Generate Python Code from Thrift File
```
thrift --gen py thrift/log_event.thrift
```

2. Start the Python Server

```
python3 server.py
```
3. Run the Python Client
```
python3 client.py
```
