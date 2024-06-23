# -*- coding: utf-8 -*-
#
# MLHub toolket for OpenAI - Supported Language of ml openai
#
# Time-stamp:
#
# Author: Ting Tang
# Licensed under GPLv3.
# Copyright (c) Togaware Pty Ltd. All rights reserved.
#
# ml supported openai

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
import click

from itertools import groupby
from whisper.tokenizer import LANGUAGES

# -----------------------------------------------------------------------
# Command line argument and options
# -----------------------------------------------------------------------
@click.command()
@click.option("--iso",
              default=False,
              is_flag=True,
              help="Get the ISO codes of all supported languages.")

def cli(iso):
    if iso:
        language_codes = sorted(LANGUAGES.keys())
        
        # Group the sorted language codes by their initial letters, 
        # and convert each group of codes to a list for later use.
        grouped = [(key, list(group)) for key, group in groupby(language_codes, key=lambda x: x[0])]
        total_groups = len(grouped)

        for index, (_, group) in enumerate(grouped):
            if index == total_groups - 1:  # Check if it's the last group
                print(",".join(group))  # Print without trailing comma
            else:
                print(",".join(group) + ",")  # Print with trailing comma

    else:
        capitalized_languages = sorted([value.capitalize() for value in LANGUAGES.values()])
        for language in capitalized_languages:
            print(language)

if __name__ == "__main__":
    cli(prog_name="supported")