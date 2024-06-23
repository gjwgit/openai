# -*- coding: utf-8 -*-
#
# MLHub toolkit for OpenAI - Audio Processing
# Shared functionalities for transcription and translation
#
# Time-stamp:
#
# Author: Graham.Williams@togaware.com, Ting Tang
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

import os
import sys
import whisper
from mlhub.pkg import get_cmd_cwd
from output_handler import OutputHandler


def process_audio(filename, lang, format, output, task):
    pkg = "openai"
    cmd = "transcribe"

    # -----------------------------------------------------------------------
    # Load the required model. Just small for now.
    # -----------------------------------------------------------------------
    model = whisper.load_model("small")

    if not filename:
        sys.exit(f"{pkg} {cmd}: A filename is required.")
        
    path = os.path.join(get_cmd_cwd(), filename)

    if not os.path.exists(path):
        sys.exit(f"{pkg} {cmd}: File not found: {path}")

    if output:
        output_path = os.path.join(get_cmd_cwd(), output)
        if os.path.exists(output_path):
            sys.exit(f"{pkg} {cmd}: Output file already exists: {output}")

    # -----------------------------------------------------------------------
    # Perform the transcribe or translate (fp16 not supported on CPU).
    # -----------------------------------------------------------------------
    result = model.transcribe(path, fp16=False, task=task, language=lang)
    
    # -----------------------------------------------------------------------
    # Handle and output the result.
    # -----------------------------------------------------------------------
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
