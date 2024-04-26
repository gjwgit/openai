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
# Copied and modified based on functions from OpenAI's whisper package,
# https://github.com/openai/whisper/blob/main/whisper/utils.py
# -----------------------------------------------------------------------

# Utility function to format timestamps
def format_timestamp(seconds: float, format_type: str = "srt"):
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    if format_type == "srt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03d}"
    elif format_type == "vtt":
        hours_marker = f"{hours:02d}:" if hours > 0 else ""
        return f"{hours_marker}{int(minutes):02}:{int(seconds):02}.{milliseconds:03d}"

# Output Handler Class
class OutputHandler:
    def __init__(self, format, output_path=None):
        self.format = format
        self.output_path = output_path

    def _output_txt(self, result, file):
        for segment in result["segments"]:
            print(segment["text"].strip(), file=file, flush=True)

    def _output_json(self, result, file):
        json.dump(result, file, indent=2)

    def _output_srt(self, result, file):
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"], "srt")
            end = format_timestamp(segment["end"], "srt")
            print(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n", file=file, flush=True)

    def _output_vtt(self, result, file):
        print("WEBVTT\n", file=file)
        for segment in result["segments"]:
            start = format_timestamp(segment["start"], "vtt")
            end = format_timestamp(segment["end"], "vtt")
            print(f"{start} --> {end}\n{segment['text'].strip()}\n", file=file, flush=True)

    def _output_tsv(self, result, file):
        print("start", "end", "text", sep="\t", file=file)
        for segment in result["segments"]:
            print(round(1000 * segment["start"]), file=file, end="\t")
            print(round(1000 * segment["end"]), file=file, end="\t")
            print(segment["text"].strip().replace("\t", " "), file=file, flush=True)

    def write(self, result):
        # Dynamically select the appropriate output method.
        # If a method for the specified format does not exist, default to txt.
        output_func = getattr(self, f"_output_{self.format}", self._output_txt)

        if self.output_path:
            with open(self.output_path, "w", encoding="utf-8") as f:
                output_func(result, f)
            print(f"Transcribed text saved to {self.output_path}", file=sys.stderr)
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
              help="The format of the output. Supported formats are txt, json, srt, tsv, and vtt.")
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="The name and format of the output file. e.g. output.txt, tmp.vtt")

def cli(filename, lang, format, output):
    """
    Transcribe audio from a file.

    Tested with wav, mp4, mov.

    The audio is processed locally using a downloaded OpenAI model The
    result is returned as text.

    Use the `-l` or `--lang` option to specify the language of the source audio.

    Use the `-f` or `--format` option to specify the desired output format. 
    Supported formats are txt, json, srt, tsv, and vtt.
    (e.g. `-f txt`).

    To save the transcribed text to a file, 
    Use the `-o` or `--output` option to specify the desired output file name 
    and format (e.g. `-o output.txt`), 

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

    # Check if the output file already exists
    if output and os.path.exists(output):
        sys.exit(f"{pkg} {cmd}: File already exists: {output}")
        
    # fp16 not supported on CPU
    result = model.transcribe(path, fp16=False, language=lang)

    if format or output:
        output_format = format if format else output.split(".")[-1]
        output_path = os.path.join(get_cmd_cwd(), output) if output else None
        output_handler = OutputHandler(output_format, output_path)
        output_handler.write(result)
    else: 
        text_buffer = [] # Buffer for accumulating segments of one sentence.
        
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
