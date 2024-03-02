# An MLHub package for OpenAI

This [MLHUB](https://mlhub.ai/) package provides a command line tool
from [whispher](https://github.com/openai/whisper) for transcribing
speech from an audio file. 

## Usage

* To install mlhub (Ubuntu 23.10 LTS)
  ```bash
  pip3 install mlhub
  ml configure
  ```

* To install and configure the package
  ```bash
  ml install gjwgit/openai@main
  ml configure openai
  ml readme openai
  ml commands openai
  ```
* Command line tools
  ```bash
  ml transcribe openai myspeech.wav
  ml translate openai myspeech.wav
  ```

* Quick test

  ```bash
  wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
  ml transcribe openai harvard.wav
  ```

to see

  ```console
  The stale smell of old beer lingers. 
  It takes heat to bring out the odor. 
  A cold dip restores health and zest. 
  A salt pickle tastes fine with ham. 
  Tacos al pastor are my favorite. 
  A zestful food is the hot cross bun.
  ```

## Options

* `-l`, `--lang`: Specify the language of the source audio to speed up the transcribe/translate process.  
For example, to transcribe audio in English, use `-l en`.  
See [tokenizer.py](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py) for the list of all available languages.

* `-o`, `--output`: Specify the output file name and format.  
For example, `-o output.txt` will save the transcribed text to a file named `output.txt` in the same directory.

Format:  
`ml transcribe openai [FILENAME] [-l LANGUAGE] [-o OUTPUT_FILE]`  
`ml translate openai [FILENAME] [-l LANGUAGE] [-o OUTPUT_FILE]`

Examples:
```bash
ml transcribe openai myspeech.wav -l en -o output.txt
ml translate openai myspeech.wav -l en -o output.txt
```

