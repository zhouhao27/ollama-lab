# Integrate MeloTTS to Ollama

MeloTTS is a free and open-source text-to-speech engine that can be used to generate speech from text. Here I integrate MeloTTS to Ollama.

## Install MeloTTS

- Run: `brew install mecab` before install `MeloTTS`
- Install inside the `poetry shell`

```bash
$ git clone https://github.com/myshell-ai/MeloTTS.git

$ cd MeloTTS

$ pip install -e .

$ python -m unidic download 
```

## Dependencies

- `langdetect` added in parent folder by `poetry add langdetect`
- `simpleaudio` added in parent folder by `poetry add simpleaudio`