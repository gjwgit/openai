# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Translate to English
#
# Time-stamp: <Sunday 2023-11-26 13:40:46 +1100 Graham Williams>
#
# Author: Graham.Williams@togaware.com
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

from mlhub.pkg import get_cmd_cwd

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
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="The name and format of the output file. e.g. output.txt")
@click.option("-f", "--format",
              default=None,
              type=click.STRING,
              help="The format of the output file. e.g. txt, json, srt")

def cli(filename, lang, output, format):
    """Translate audio from a file into English.

Tested with wav, mp4, mov.

The audio is processed locally using a downloaded OpenAI model. The
result is returned as text.

Use the `-l` or `--lang` option to specify the language of the source audio.

To save the translated text to a file, 
use the `-o` or `--output` option to specify the desired output file name and 
format (e.g. `output.txt`), 
or use the `-f` or `--format` option to specify the desired output file format
(e.g. `txt`) while the file name will be the same as input audio file name.

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
        
    result = model.transcribe(path, fp16=False, task="translate", language=lang)
    text = result["text"].strip()

    if output or format:
        output_path = (
            os.path.join(get_cmd_cwd(), output) if output 
            else os.path.join(get_cmd_cwd(), 
                              filename.replace(filename.split(".")[-1], format))
        )
        with open(output_path, "w") as f:
            f.write(text)
        print("Translated text saved to", output_path)
    else:
        print(text)
    
if __name__ == "__main__":
    cli(prog_name="translate")
