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

def cli(filename, lang):
    """Translate audio from a file into English.

Tested with wav, mp4.

The audio is processed locally using a downlaoded OpenAI model. The
result is returned as text.

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
        
    result = model.transcribe(path, fp16=False, task="translate")

    print(result["text"])
    
if __name__ == "__main__":
    cli(prog_name="translate")
