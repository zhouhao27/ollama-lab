import os
import ollama
import argparse
from tts import Speaker

parser = argparse.ArgumentParser(prog='TTS')
parser.add_argument('prompt', type=str, help='Prompt')
parser.add_argument('-m', '--model', type=str, default='llama3', help='Model')
args = parser.parse_args()

if os.path.isfile(args.prompt):
    with open(args.prompt, 'r') as f:
        prompt = f.read()
else:
    prompt = args.prompt

model = args.model

def __ollama_llm__(prompt, model): 
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

if __name__ == '__main__':
    speaker = Speaker('./output')
    response = __ollama_llm__(prompt, model)
    print(response)
    speaker.speak(response)


