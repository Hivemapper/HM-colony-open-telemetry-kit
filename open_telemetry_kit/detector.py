from .parser import Parser
import os
import json
from typing import Dict, Tuple, Union, List
JSONType = Dict[str, Union[List[Dict[str, Union[str, int]]], Dict[str,Union[str, int]]]]

def split_path(src: str) -> Tuple[str, str, str]:
  path, filename = os.path.split(src)

  if filename:
    name, ext = os.path.splitext(filename)
    return (path, name, ext.lower())

  return (path, "", "")

def read_video_metadata(src: str) -> JSONType:
  data_raw = os.popen("ffprobe -v quiet -print_format json -show_format -show_streams " + src).read()
  return json.loads(data_raw)

def write_video_metadata(metadata: JSONType, dest: str):
  with open(os.path.join(dest, "metadata.json"), 'w') as fl:
    json.dump(metadata, fl, indent=3)

def read_video_metadata_file(src: str):
  with open(src, 'r') as fl:
    metadata = json.load(fl)
  return metadata

def get_embedded_telemetry_type(metadata: JSONType) -> str:
  if "streams" in metadata:
    for stream in metadata["streams"]:
      if stream["codec_type"] == "subtitle" and stream["codec_tag_string"] == "text":
        return "srt"
      elif stream["codec_type"] == "data" and stream["codec_tag_string"] == "KLVA":
        return "klv"

  return None

# If supported return the extension and bool
#   False: Telemetry is not embedded in video file (in it's own file)
#   True: Telemetry is embedded in video file
# TODO: Rewrite so we're not doing the same search twice.
# Not a huge deal now, but as more types get supported will get worse
def get_telemetry_type(src: str) -> Tuple[str, bool]:
  _, _, tel_type = split_path(src)
  supported = [cls.ext for cls in Parser.__subclasses__()]
  if tel_type.strip('.') in supported:
    return (tel_type.strip('.'), False)
  
  metadata = read_video_metadata(src)
  tel_type = get_embedded_telemetry_type(metadata)

  if tel_type and tel_type.strip('.') in supported:
    return (tel_type, True)
  
  return (None, False)
    
def create_telemetry_parser(src: str) -> Parser:
  tel_type, embedded = get_telemetry_type(src)
  tel_src = src

  for cls in Parser.__subclasses__():
    if tel_type == cls.ext:
      if not embedded:
        return cls(tel_src)
      else:
        return cls(tel_src, is_embedded=embedded)

def read_embedded_subtitles(src: str) -> str:
  cmd = "ffmpeg -y -i " + src + " -f srt - " 
  srt = os.popen(cmd).read()
  return srt

def write_embedded_subtitles(srt: str, dest: str):
  _, tail = os.path.split(dest)
  if tail:
    with open(dest, 'w') as fl:
      fl.write(srt)
  else:
    with open(os.path.join(dest, "video.srt"), 'w') as fl:
      fl.write(srt)


