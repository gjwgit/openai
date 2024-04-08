import json
import os
import sys

# -----------------------------------------------------------------------
# Helper functions
# Copied and modified based on functions from OpenAI's whisper package,
# https://github.com/openai/whisper/blob/main/whisper/utils.py
# -----------------------------------------------------------------------

# Utility function to format timestamps
def format_timestamp(seconds: float, format_type: str = "srt"):
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    if format_type == "srt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03d}"
    elif format_type == "vtt":
        hours_marker = f"{hours:02d}:" if hours > 0 else ""
        return f"{hours_marker}{int(minutes):02}:{int(seconds):02}.{milliseconds:03d}"

# Output Handler Class
class OutputHandler:
    def __init__(self, format, output_path=None):
        self.format = format
        self.output_path = output_path

    def _output_txt(self, result, file):
        for segment in result["segments"]:
            print(segment["text"].strip(), file=file, flush=True)

    def _output_json(self, result, file):
        json.dump(result, file, indent=2)

    def _output_srt(self, result, file):
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"], "srt")
            end = format_timestamp(segment["end"], "srt")
            print(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n", file=file, flush=True)

    def _output_vtt(self, result, file):
        print("WEBVTT\n", file=file)
        for segment in result["segments"]:
            start = format_timestamp(segment["start"], "vtt")
            end = format_timestamp(segment["end"], "vtt")
            print(f"{start} --> {end}\n{segment['text'].strip()}\n", file=file, flush=True)

    def _output_tsv(self, result, file):
        print("start", "end", "text", sep="\t", file=file)
        for segment in result["segments"]:
            print(round(1000 * segment["start"]), file=file, end="\t")
            print(round(1000 * segment["end"]), file=file, end="\t")
            print(segment["text"].strip().replace("\t", " "), file=file, flush=True)

    def write(self, result):
        # Dynamically select the appropriate output method.
        # If a method for the specified format does not exist, default to txt.
        output_func = getattr(self, f"_output_{self.format}", self._output_txt)

        if self.output_path:
            if os.path.exists(self.output_path):
                # File exists, write an error message and exit with status 1
                print(f"Error: File '{self.output_path}' already exists.", file=sys.stderr)
                sys.exit(1)
            else: # File does not exist
                with open(self.output_path, "w", encoding="utf-8") as f:
                    output_func(result, f)
                print(f"Transcribed text saved to {self.output_path}", file=sys.stderr)
                sys.exit(0)
        else:
            output_func(result, sys.stdout)