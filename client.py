# -*- coding: utf-8 -*-
import grpc
import demo_pb2_grpc
import demo_pb2
import random


def invoke_calculate(stub):
    work = demo_pb2.Work()
    work.num1 = 100
    work.num2 = 20

    work.op = demo_pb2.Work.ADD
    res = stub.Calculate(work)
    print(f"100 + 20 = {res.val}")

    work.op = demo_pb2.Work.SUBTRACT
    res = stub.Calculate(work)
    print(f"100 - 20 = {res.val}")

    work.op = demo_pb2.Work.MULTIPLY
    res = stub.Calculate(work)
    print(f"100 * 20 = {res.val}")

    work.op = demo_pb2.Work.DIVIDE
    res = stub.Calculate(work)
    print(f"100 / 20 = {res.val}")

    work.num2 = 0
    try:
        res = stub.Calculate(work)
        print(f"100 / 0 = {res.val}")
    except grpc.RpcError as e:
        print(f"{e.code()}: {e.details()}")

def invoke_get_subjects(stub):
    city = demo_pb2.City(name="beijing")
    subjects = stub.GetSubjects(city)
    for subject in subjects:
        print(subject.name)

def generate_delta():
    for i in range(10):
        delta = random.randint(1, 100)
        if i == 9:
            print(delta)
        else:
            print(delta, end=", ")
        yield demo_pb2.Delta(val=delta)

def invoke_accumulate(stub):
    delta_iterator = generate_delta()
    sum = stub.Accumulate(delta_iterator)
    print(f"sum={sum.val}")

def generate_number():
    for i in range(10):
        number = random.randint(1, 100)
        print(number)
        yield demo_pb2.Number(val=number)

def invoke_guess_number(stub):
    number_iterator = generate_number()
    answers = stub.GuessNumber(number_iterator)
    for answer in answers:
        print(f"{answer.desc}: {answer.val}")

def run():
    with grpc.insecure_channel("127.0.0.1:8888") as channel:
        # 创建辅助客户端调用的stub对象
        stub = demo_pb2_grpc.DemoStub(channel)
        # invoke_calculate(stub)
        # invoke_get_subjects(stub)
        # invoke_accumulate(stub)
        invoke_guess_number(stub)

if __name__ == '__main__':
    run()