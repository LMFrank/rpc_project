## simple_grpc

gRPC是由Google公司开源的高性能RPC框架，它支持多语言、多平台的使用。它的消息协议使用Google开源的Protocol Buffers协议机制（proto3），传输使用HTTP/2标准，支持双向流和连接多路复用。

### 接口类型

- **Unary RPC** （一元RPC）
- **Server Streaming RPC** （ 服务器流式RPC）
- **Client Streaming RPC** （ 客户端流式RPC）
- **Bidirectional Streaming RPC** （双向流式RPC）

### 安装依赖

```shell
pip install grpcio-tools
```

### 使用方法

在本项目中，使用4个不同的案例演示4种接口类型的调用。

1. 使用Protocol Buffers（proto3）的IDL接口定义语言定义接口服务，编写在文本文件（以`.proto`为后缀名）中，然后运行以下命令编译生成python代码

   ```shell
   python -m grpc_tools.protoc -I. --python_out=.. --grpc_python_out=.. demo.proto
   ```
- `-I`表示搜索proto文件中被导入文件的目录
- `--python_out`表示保存生成Python文件的目录，生成的文件中包含接口定义中的数据类型
- `--grpc_python_out`表示保存生成Python文件的目录，生成的文件中包含接口定义中的服务类型

2. 编写补充服务器和客户端逻辑代码 