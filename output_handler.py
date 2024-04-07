import json
import sys

# Utility function to format timestamps
def format_timestamp(seconds: float, format_type: str = "srt"):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(seconds % 1 * 1000)
    if format_type == "srt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03d}"
    elif format_type == "vtt":
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03d}"

# Output Handler Class
class OutputHandler:
    def __init__(self, format, output_path=None):
        self.format = format
        self.output_path = output_path

    def _output_txt(self, result, file):
        for segment in result["segments"]:
            print(segment["text"].strip(), file=file)

    def _output_json(self, result, file):
        json.dump(result, file, indent=4)

    def _output_srt(self, result, file):
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"], "srt")
            end = format_timestamp(segment["end"], "srt")
            print(f"{i}\n{start} --> {end}\n{segment['text'].strip()}\n", file=file)

    def _output_vtt(self, result, file):
        print("WEBVTT\nKind: captions\nLanguage: en\n", file=file)
        for segment in result["segments"]:
            start = format_timestamp(segment["start"], "vtt")
            end = format_timestamp(segment["end"], "vtt")
            print(f"{start} --> {end}\n{segment['text'].strip()}\n", file=file)

    def _output_tsv(self, result, file):
        for segment in result["segments"]:
            start_ms = int(segment["start"] * 1000)
            end_ms = int(segment["end"] * 1000)
            print(f"{start_ms}\t{end_ms}\t{segment['text'].strip()}", file=file)

    def write(self, result):
        output_func = getattr(self, f"_output_{self.format}", self._output_txt)
        if self.output_path:
            with open(self.output_path, "w", encoding="utf-8") as f:
                output_func(result, f)
            print(f"Transcribed text saved to {self.output_path}")
        else:
            output_func(result, sys.stdout)