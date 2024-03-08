# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Identify
#
# Time-stamp:
#
# Author:
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.
#
# ml identify openai

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

def cli(filename):
    """Identify the language of a media file.

The audio is processed locally using a downloaded OpenAI model. The
result is returned as text.

    """

    pkg = "openai"
    cmd = "identify"

    # -----------------------------------------------------------------------
    # Load the required model. Just small for now.
    # -----------------------------------------------------------------------

    model = whisper.load_model("small")

    # -----------------------------------------------------------------------
    # Identify the language of the file.
    # -----------------------------------------------------------------------

    if not filename:
        sys.exit(f"{pkg} {cmd}: A filename is required.")
        
    path = os.path.join(get_cmd_cwd(), filename)

    if not os.path.exists(path):
        sys.exit(f"{pkg} {cmd}: File not found: {path}")
        
    result = model.transcribe(path, fp16=False)
    language = result["language"].strip()
    print(language)
    
if __name__ == "__main__":
    cli(prog_name="identify")
