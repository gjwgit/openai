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

languages = """
Afrikaans
Albanian
Amharic
Arabic
Armenian
Assamese
Azerbaijani
Bashkir
Basque
Belarusian
Bengali
Bosnian
Breton
Bulgarian
Cantonese
Catalan
Chinese
Croatian
Czech
Danish
Dutch
English
Estonian
Faroese
Finnish
French
Galician
Georgian
German
Greek
Gujarati
Haitian creole
Hausa
Hawaiian
Hebrew
Hindi
Hungarian
Icelandic
Indonesian
Italian
Japanese
Javanese
Kannada
Kazakh
Khmer
Korean
Lao
Latin
Latvian
Lingala
Lithuanian
Luxembourgish
Macedonian
Malagasy
Malay
Malayalam
Maltese
Maori
Marathi
Mongolian
Myanmar
Nepali
Norwegian
Nynorsk
Occitan
Pashto
Persian
Polish
Portuguese
Punjabi
Romanian
Russian
Sanskrit
Serbian
Shona
Sindhi
Sinhala
Slovak
Slovenian
Somali
Spanish
Sundanese
Swahili
Swedish
Tagalog
Tajik
Tamil
Tatar
Telugu
Thai
Tibetan
Turkish
Turkmen
Ukrainian
Urdu
Uzbek
Vietnamese
Welsh
Yiddish
Yoruba
"""

iso_codes = """
af,am,ar,as,az,
ba,be,bg,bn,bo,br,bs,
ca,cs,cy,
da,de,
el,en,es,et,eu,
fa,fi,fo,fr,
gl,gu,
ha,haw,he,hi,hr,ht,hu,hy,
id,is,it,
ja,jw,
ka,kk,km,kn,ko,
la,lb,ln,lo,lt,lv,
mg,mi,mk,ml,mn,mr,ms,mt,my,
ne,nl,nn,no,
oc,
pa,pl,ps,pt,
ro,ru,
sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,
ta,te,tg,th,tk,tl,tr,tt,
uk,ur,uz,
vi,
yi,yo,yue,
zh
"""

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
        print(iso_codes.strip())
    else:
        print(languages.strip())

if __name__ == "__main__":
    cli(prog_name="supported")