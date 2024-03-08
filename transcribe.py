# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Transcribe
#
# Time-stamp: <Sunday 2023-11-26 14:06:57 +1100 Graham Williams>
#
# Author: Graham.Williams@togaware.com
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
              help="The language of the source audio.")
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="Output file name and format. e.g. output.txt, output.json")

def cli(filename, lang, output):
    """Transcribe audio from a file.

Tested with wav, mp4, mov.

The audio is processed locally using a downloaded OpenAI model The
result is returned as text.

Use the `-l` or `--lang` option to specify the language of the source audio.

To save the transcribed text to a file, use the `-o` or `--output` option to 
specify the desired output file name and format (e.g. `output.txt`).

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
    text = result["text"].strip()

    if output:
        output_path = os.path.join(get_cmd_cwd(), output)
        with open(output_path, "w") as f:
            f.write(text)
        print("Transcribed text saved to", output_path)
    else:
        print(text)

if __name__ == "__main__":
    cli(prog_name="transcribe")
