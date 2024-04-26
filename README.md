# An MLHub package for OpenAI

This [MLHUB](https://mlhub.ai/) package provides a command line tool
based on [whispher](https://github.com/openai/whisper) for
transcribing speech from an audio file. See the [MLHub Desktop
Survival Guide](https://survivor.togaware.com/mlhub/openai.html) for details.

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
  ml identify openai myspeech.wav
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

* `-l`, `--lang`: Specify the language of the source audio.  
This will speed up the transcribe/translate process.  
See [tokenizer.py](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py) 
for the list of all available languages.

* `-f`, `--format`: Specify the output format.  
Supported formats are **txt, json, srt, tsv, and vtt**. Read more about formatting on 
[MLHub Survival Guide](https://survivor.togaware.com/mlhub/openai-transcribe-output-formats.html).  
For example, `-f json` will format the output text to the json format.

* `-o`, `--output`: Specify the output file name and format.  
For example, `-o output.txt` will save the output text as the txt format to a 
file named `output.txt` in the same directory.

*Without `-o`, then by default, the output text will be printed in the console.*

Format:  
`ml transcribe openai [-l LANGUAGE] [-f FORMAT] [FILENAME]`  
`ml translate openai [-l LANGUAGE] [-o OUTPUT_FILENAME_AND_FORMAT] [FILENAME]`

Examples:
```bash
ml transcribe openai -l en -f txt myspeech.wav 
ml translate openai --output jokowi.srt --lang id jokowi.wav
```
