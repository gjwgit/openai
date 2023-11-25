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
  $ ml install gjwgit/openai
  $ ml configure openai
  $ ml readme openai
  $ ml commands openai
  ```
* Command line tools
  ```console
  $ ml transcribe openai myspeech.wav
  ```
