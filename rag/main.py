import os
from RAG import RAG
import argparse

### Reference: https://youtu.be/O7RdEyRsatw?list=PLYQsp-tXX9w5A0gsQ0iaJead_HvMzyl2M
#### Usage
parser = argparse.ArgumentParser(prog='RAG')
parser.add_argument('path', type=str, help='Document path')
parser.add_argument('-p', '--prompt', default="You're are very helpful assistant",  type=str, help='System prompt')
args = parser.parse_args()

if not os.path.exists(args.path) and not RAG.is_valid_url(args.path):
    exit("Invalid path")

if os.path.exists(args.prompt):
    prompt = open(args.prompt, 'r').read()
else:
    prompt = args.prompt

# example 1: python main.py ./data/matches.txt
# question = '2024欧洲杯足球比赛，德国和匈牙利比赛的比分是多少？'
# question = input('请输入2024欧洲杯A组比赛相关问题: ')

# example 2: python main.py 'https://www.propertyguru.com.sg/new-project-launch' -p ./data/property_prompt.txt
question = input('请输入有关最新新加坡租屋市场的问题: ')

rag = RAG(args.path, question, prompt)

print(f'Your data path: {args.path}\n')
print(f'Your question: {question}\n')

# print('------------ Before RAG ------------')
# print(rag.query_without_rag())
print('------------ After RAG ------------')
print(rag.query())



