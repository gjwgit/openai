# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Identify the language of a media file.
#
# Time-stamp:
#
# Author: Ting Tang
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
from whisper.tokenizer import LANGUAGES

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------

@click.command()
@click.argument("filename",
                default=None,
                required=False,
                type=click.STRING)

def cli(filename):
    """
    Identify the language of a media file.

    Tested with wav, mp3, mov.

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
        
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    language_code = max(probs, key=probs.get)
    language = language_code + "," + LANGUAGES[language_code].title()
    print(language)
    
if __name__ == "__main__":
    cli(prog_name="identify")
