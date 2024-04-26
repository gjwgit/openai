# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Translate to English
#
# Time-stamp: <Sunday 2023-11-26 13:40:46 +1100 Graham Williams>
#
# Author: Graham.Williams@togaware.com, Ting Tang
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.
#
# ml translate openai

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import os
import sys
import click
import whisper
import json

from mlhub.pkg import get_cmd_cwd
from output_handler import OutputHandler

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
              help="The language of the source audio (auto).")
@click.option("-f", "--format",
              default=None,
              type=click.STRING,
              help="The format of the output. Supported formats are txt, json, srt, tsv, and vtt.")
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="The name and format of the output file. e.g. output.txt, tmp.vtt")

def cli(filename, lang, output, format):
    """
    Translate audio from a file into English.

    Tested with wav, mp4, mov.

    The audio is processed locally using a downloaded OpenAI model. The
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
    cmd = "translate"

    # -----------------------------------------------------------------------
    # Load the required model. Just small for now.
    # -----------------------------------------------------------------------

    model = whisper.load_model("small")

    # -----------------------------------------------------------------------
    # Translate file.
    # -----------------------------------------------------------------------

    if not filename:
        sys.exit(f"{pkg} {cmd}: A filename is required.")
        
    path = os.path.join(get_cmd_cwd(), filename)

    if not os.path.exists(path):
        sys.exit(f"{pkg} {cmd}: File not found: {path}")

    # Check if the output file already exists
    if output:
        output_path = os.path.join(get_cmd_cwd(), output)
        if os.path.exists(output_path):
            sys.exit(f"{pkg} {cmd}: Output file already exists: {output}")
        
    result = model.transcribe(path, fp16=False, task="translate", language=lang)

    if format or output:
        output_format = format if format else output.split(".")[-1]
        output_handler = OutputHandler(output_format, output_path if output else None)
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
    cli(prog_name="translate")
