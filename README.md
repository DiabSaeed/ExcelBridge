# ExcelBridge
An open-source, thin-client SDK that bridges Microsoft Excel VBA with modern cloud data platforms, starting with Databricks.

ExcelBridge empowers VBA developers to interact with advanced data platforms seamlessly, completely abstracting the complexities of REST APIs, authentication protocols, JSON parsing, and platform-specific SDKs.

## Why ExcelBridge?

While solutions like ODBC/JDBC drivers and Power Query exist, they introduce significant enterprise challenges:

- ODBC Drivers: Require local installation and configuration on every user's machine (an IT maintenance nightmare).

- Power Query: Highly efficient for data retrieval (Read-only) but incapable of executing operational commands like triggering Databricks Notebooks or running enterprise Jobs.

- xlwings: Requires a local Python runtime on the client machine for its open-source version.

ExcelBridge solves this by utilizing a Centralized API Gateway architecture. The Excel client remains incredibly lightweight (Thin Client) and communicates via standard HTTP/JSON with a high-performance Python backend, isolating enterprise security and database drivers to the server side.


## High-Level Architecture

┌────────────────────────────────────────────────────────┐
│                      Excel Client                      │
│   (VBA Class Modules - Thin Client - Facade Pattern)    │
└───────────────────────────┬────────────────────────────┘
                            │
                        HTTP / JSON
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                 Python API Gateway                     │
│               (FastAPI - Routing Layer)                │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Connector Factory                    │
│              (Creational Design Pattern)               │
└───────────────────────────┬────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌───────────────┐ ┌────────────────┐
│Databricks Conn. │ │ Fabric Conn.  │ │Snowflake Conn. │
│(Strategy/Adapter)││  (Future V0.3)│ │ (Future V0.4)  │
└────────┬────────┘ └───────┬───────┘ └───────┬────────┘
         │                  │                 │
         └──────────────────┼─────────────────┘
                            │
                            ▼
               [ Cloud Data Platforms ]

