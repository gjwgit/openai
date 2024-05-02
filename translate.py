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

import click
from audio_processing import process_audio

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
    Translate audio from a file into English.

    Tested with mp3, wav, mp4, mov.

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
    process_audio(filename, lang, format, output, task="translate")

    
if __name__ == "__main__":
    cli(prog_name="translate")
