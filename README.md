# An MLHub package for OpenAI

This [MLHUB](https://mlhub.ai/) package provides a command line tool
from [whispher](https://github.com/openai/whisper) for transcribing
speech from an audio file. 

## Usage

* To install mlhub (Ubuntu 23.10 LTS)
  ```console
  $ pip3 install mlhub
  $ ml configure
  ```

* To install and configure the package
  ```console
  $ ml install gjwgit/openai@main
  $ ml configure openai
  $ ml readme openai
  $ ml commands openai
  ```
* Command line tools
  ```console
  $ ml transcribe openai myspeech.wav
  ```

* Quick test

  ```console
  wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
  ml transcribe openai harvard.wav
  ```

to see

  ```
  The stale smell of old beer lingers. 
  It takes heat to bring out the odor. 
  A cold dip restores health and zest. 
  A salt pickle tastes fine with ham. 
  Tacos al pastor are my favorite. 
  A zestful food is the hot cross bun.
  ```
