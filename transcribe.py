# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Transcribe
#
# Time-stamp: <Sunday 2023-11-26 14:06:57 +1100 Graham Williams>
#
# Author: Graham.Williams@togaware.com, Ting Tang
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.
#
# ml transcribe openai

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import os
import sys
import click
import whisper
import json

from mlhub.pkg import get_cmd_cwd
# from .output_handler import OutputHandler

# -----------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------

# Utility function to format timestamps
def format_timestamp(seconds: float, format_type: str = "srt"):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(seconds % 1 * 1000)
    if format_type == "srt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03d}"
    elif format_type == "vtt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03d}"

# Output Handler Class
class OutputHandler:
    def __init__(self, format, output_path=None):
        self.format = format
        self.output_path = output_path

    def _output_txt(self, result, file):
        for segment in result["segments"]:
            print(segment["text"].strip(), file=file)

    def _output_json(self, result, file):
        json.dump(result, file, indent=4)

    def _output_srt(self, result, file):
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"], "srt")
            end = format_timestamp(segment["end"], "srt")
            print(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n", file=file)

    def _output_vtt(self, result, file):
        print("WEBVTT\nKind: captions\nLanguage: en\n", file=file)
        for segment in result["segments"]:
            start = format_timestamp(segment["start"], "vtt")
            end = format_timestamp(segment["end"], "vtt")
            print(f"{start} --> {end}\n{segment['text'].strip()}\n", file=file)

    def _output_tsv(self, result, file):
        for segment in result["segments"]:
            start_ms = int(segment["start"] * 1000)
            end_ms = int(segment["end"] * 1000)
            print(f"{start_ms}\t{end_ms}\t{segment['text'].strip()}", file=file)

    def write(self, result):
        output_func = getattr(self, f"_output_{self.format}", self._output_txt)
        if self.output_path:
            with open(self.output_path, "w", encoding="utf-8") as f:
                output_func(result, f)
            print(f"Transcribed text saved to {self.output_path}")
        else:
            output_func(result, sys.stdout)

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("filename",
                default=None,
                required=False,
                type=click.STRING)
@click.option("-l", "--lang",
              default=None,
              type=click.STRING,
              help="The language of the source audio.")
@click.option("-f", "--format",
              default=None,
              type=click.STRING,
              help="The format of the output. e.g. txt, json, srt")
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="The name and format of the output file. e.g. output.txt")

def cli(filename, lang, format, output):
    """
    Transcribe audio from a file.

    Tested with wav, mp4, mov.

    The audio is processed locally using a downloaded OpenAI model The
    result is returned as text.

    Use the `-l` or `--lang` option to specify the language of the source audio.

    Use the `-f` or `--format` option to specify the desired output format
    (e.g. `txt`).

    To save the transcribed text to a file, 
    use the `-o` or `--output` option to specify the desired output file name 
    and format (e.g. `output.txt`), 

    """
    pkg = "openai"
    cmd = "transcribe"

    # -----------------------------------------------------------------------
    # Load the required model. Just small for now.
    # -----------------------------------------------------------------------

    model = whisper.load_model("small")

    # -----------------------------------------------------------------------
    # Transcribe file or from microphone.
    # -----------------------------------------------------------------------

    if not filename:
        sys.exit(f"{pkg} {cmd}: A filename is required.")
        
    path = os.path.join(get_cmd_cwd(), filename)

    if not os.path.exists(path):
        sys.exit(f"{pkg} {cmd}: File not found: {path}")
        
    # fp16 not supported on CPU
    result = model.transcribe(path, fp16=False, language=lang)

    text_buffer = [] # Buffer for accumulating segments of one sentence.

    if format or output:
        output_handler = OutputHandler(format, output_path=os.path.join(get_cmd_cwd(), output) if output else None)
        output_handler.write(result)
    else: 
        # If no format or output is specified, 
        # print the text to the console as one sentence per line.
        for segment in result["segments"]:
            text_buffer.append(segment["text"].strip())
            
            if segment["text"].strip()[-1] in [".", "?", "!", "。", "？", "！"]:
                # Reached the end of a sentence.
                full_sentence = " ".join(text_buffer)
                print(full_sentence)
                text_buffer = []
        
        # Handle the remaining text in the buffer.
        if text_buffer:
            trailing_text = " ".join(text_buffer)
            print(trailing_text)
    
if __name__ == "__main__":
    cli(prog_name="transcribe")
