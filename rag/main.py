import os
from RAG import RAG
import argparse

### Reference: https://youtu.be/O7RdEyRsatw?list=PLYQsp-tXX9w5A0gsQ0iaJead_HvMzyl2M
#### Usage
parser = argparse.ArgumentParser(prog='RAG')
parser.add_argument('path', type=str, help='Document path')
args = parser.parse_args()

if not os.path.exists(args.path):
    exit("Invalid path")

# question = '2024欧洲杯足球比赛，德国和匈牙利比赛的比分是多少？'
question = input('请输入2024欧洲杯A组比赛相关问题: ')
rag = RAG(args.path, question)

print(f'Your data path: {args.path}\n')
print(f'Your question: {question}\n')

print('------------ Before RAG ------------')
print(rag.query_without_rag())
print('------------ After RAG ------------')
print(rag.query_with_rag())

