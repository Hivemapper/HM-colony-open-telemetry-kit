from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import UnknownElement
# from .elements import LatitudeElement, LongitudeElement, AltitudeElement
from .elements import TimestampElement, ChecksumElement
from .misb_0601 import MISB_0601
from .detector import read_video_metadata, read_klv
from .klv_common import bytes_to_int

from io import BytesIO
import xml.etree.ElementTree as ET
from dateutil import parser as dup
import logging
import os
from typing import List

class KLVParser(Parser):
  tel_type = 'klv'
  keys = {bytes.fromhex("06 0E 2B 34 02 0B 01 01 0E 01 03 01 01 00 00 00") : "misb" ,
          bytes.fromhex("06 0E 2B 34 01 01 01 01 0F 00 00 00 00 00 00 00") : "old_misb"}

  def __init__(self, source: str,
               is_embedded: bool = True):
    self.source = source
    self.element_dict = {}
    
    for cls in MISB_0601.__subclasses__():
      self.element_dict[cls.misb_tag] = cls

  def read(self):
    metadata = read_video_metadata(self.source)
    klv = read_klv(self.source, metadata)
    self.klv_stream = BytesIO(klv)

    return self._parse()
    
  def _parse(self):
    stream_end = self.klv_stream.seek(0, os.SEEK_END)
    self.klv_stream.seek(0, os.SEEK_SET)
    packet_start = 0
    key = self.klv_stream.read(16)
    tel = Telemetry()
    while self.klv_stream.tell() != stream_end:
      if key in self.keys:
        if self.keys[key] in ["misb", "old_misb"]:
          packet_len = self._read_len()
          packet_end = self.klv_stream.tell() + packet_len
          if not self._parse_misb_packet(tel, packet_end):
            self.klv_stream.seek(packet_start + 1, os.SEEK_SET)
      else:
        self.klv_stream.seek(-15, os.SEEK_CUR)

      packet_start = self.klv_stream.tell()
      key = self.klv_stream.read(16)

    return tel

  def _parse_misb_packet(self, tel, packet_end):
    packet = Packet()

    first_packet = True
    while self.klv_stream.tell() != packet_end:
      tag = self._read_tag()

      if first_packet and tag != TimestampElement.misb_tag:
        # Per MISB 0601 standard, first tag must be timestamp
        # TODO: add error
        break
      first_packet = False

      elem_len = self._read_len()
      if self.klv_stream.tell() + elem_len > packet_end:
        #TODO: add error
        break

      value = self.klv_stream.read(elem_len)

      if tag in self.element_dict:
        packet[self.element_dict[tag].misb_name] = self.element_dict[tag].fromMISB(value)
      else: 
        packet["Tag " + str(tag)] = UnknownElement(value)

    if self.klv_stream.tell() == packet_end:
      tel.append(packet)
      return True
    else:
      #TODO add error
      return False

  def _read_len(self):
    length = bytes_to_int(self.klv_stream.read(1))

    if length >= 128:
      length = bytes_to_int(self.klv_stream.read(length - 128))

    return length

  def _read_tag(self):
    tag_byte = bytes_to_int(self.klv_stream.read(1))

    if tag_byte < 128:
      return tag_byte

    tag = 0
    while tag_byte >= 128:
      tag = (tag << 7) + (tag_byte - 128)
      tag_byte = bytes_to_int(self.klv_stream.read(1))

    tag = (tag << 7) + (tag_byte)
    return tag
    

