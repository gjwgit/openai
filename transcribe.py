# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Transcribe
#
# Time-stamp: 
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
@click.option("-f", "--format",
              default=None,
              type=click.STRING,
              help="The format of the output. e.g. txt, json, srt")
@click.option("-o", "--output",
              default=None,
              type=click.STRING,
              help="The name and format of the output file. e.g. output.txt")

def cli(filename, lang, output, format):
    """
    Transcribe audio from a file.

    Tested with wav, mp4, mov.

    The audio is processed locally using a downloaded OpenAI model The
    result is returned as text.

    Use the `-l` or `--lang` option to specify the language of the source audio.

    To save the transcribed text to a file, 
    use the `-o` or `--output` option to specify the desired output file name and 
    format (e.g. `output.txt`), 
    or use the `-f` or `--format` option to specify the desired output file format
    (e.g. `txt`) while the file name will be the same as input audio file name.

    """
    pkg = "openai"
    cmd = "transcribe"

    if not filename:
        sys.exit(f"{pkg} {cmd}: A filename is required.")
        
    path = os.path.join(get_cmd_cwd(), filename)

    if not os.path.exists(path):
        sys.exit(f"{pkg} {cmd}: File not found: {path}")

    # Define the command we want to run using Whisper
    command = "whisper " + filename + " --model small"

    # Use os.system to execute the command
    status = os.system(command)

    # Check if the command was executed successfully
    if status == 0:
        print("Command executed successfully!")
    else:
        print("Command execution failed!")

if __name__ == "__main__":
    cli(prog_name="transcribe")
