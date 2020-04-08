# -*- coding: utf-8 -*-
import demo_pb2_grpc
import demo_pb2
import grpc
import time
from concurrent import futures


class DemoServicer(demo_pb2_grpc.DemoServicer):

    def __init__(self):
        self.city_subjects_db = {
            "beijing": ["python", "c++", "go", "java", "php"],
            "shanghai": ["python", "c++", "go", "c"],
            "shenzhen": ["python", "vue", "c"]
        }
        self.answers = list(range(10))

    def Calculate(self, request, context):
        if request.op == demo_pb2.Work.ADD:
            result = request.num1 + request.num2
            return demo_pb2.Result(val=result)
        elif request.op == demo_pb2.Work.SUBTRACT:
            result = request.num1 - request.num2
            return demo_pb2.Result(val=result)
        elif request.op == demo_pb2.Work.MULTIPLY:
            result = request.num1 * request.num2
            return demo_pb2.Result(val=result)
        elif request.op == demo_pb2.Work.DIVIDE:
            if request.num2 == 0:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('cannot divide by 0')
                return demo_pb2.Result()
            result = request.num1 // request.num2
            return demo_pb2.Result(val=result)
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('invalid operation')
            return demo_pb2.Result()

    def GetSubjects(self, request, context):
        city = request.name
        subjects = self.city_subjects_db.get(city)
        for subject in subjects:
            yield demo_pb2.Subject(name=subject)

    def Accumulate(self, request_iterator, context):
        sum = 0
        for request in request_iterator:
            sum += request.val
        return demo_pb2.Sum(val=sum)

    def GuessNumber(self, request_iterator, context):
        for request in request_iterator:
            if request.val in self.answers:
                yield demo_pb2.Answer(val=request.val, desc="Yes!")

def serve():
    # 创建服务器对象，多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 注册服务方法到服务器对象
    demo_pb2_grpc.add_DemoServicer_to_server(DemoServicer(), server)

    # 设置服务器地址
    server.add_insecure_port("127.0.0.1:8888")

    # 开启服务
    print("服务器已开启...")
    server.start()

    # 关闭服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
        
