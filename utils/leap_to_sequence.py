import numpy as np
import os
import sys

HAND_MAP = {
  "left": "Left",
  "right": "Right"
}
FINGER_MAP = {
  "0": "Thumb",
  "1": "Index",
  "2": "Middle",
  "3": "Ring",
  "4": "Pinky"
}
JOINT_MAP = {
  "0": "CMC",
  "1": "MCP",
  "2": "PIP",
  "3": "DIP",
  "4": "TIP"
}
TIME_STRING = "time"

def leap_file_to_sequence_files(filepath, temporal_offset):
  transform_dict = {}
  curr_timestamp = 0
  with open(leap_filepath, "r") as leap_file:
    for curr_line in leap_file:
      curr_parts = curr_line.split(";")

      for curr_entry in curr_parts:
        curr_entry = curr_entry.strip()
        if curr_entry == "":
          continue
        entry_key, entry_value = get_entry_key_value(curr_entry)
        if entry_key == TIME_STRING:
          curr_timestamp = float(entry_value) / 1e6 + temporal_offset # sampling times are in microseconds
          break

      for curr_entry in curr_parts:
        curr_entry = curr_entry.strip()
        if curr_entry == "":
          continue
        entry_key, entry_value = get_entry_key_value(curr_entry)
        if entry_key == TIME_STRING:
          continue
        curr_transform_name = leap_name_to_transform_name(entry_key)
        curr_transform_string = position_string_to_transform_string(entry_value)

        if curr_transform_name in transform_dict:
          transform_dict[curr_transform_name].append((curr_timestamp, curr_transform_string))
        else:
          transform_dict[curr_transform_name] = [(curr_timestamp, curr_transform_string)]

  for transform_name, transform_values in transform_dict.items():
    print(transform_name)
    num_transforms = len(transform_values)
    with open(transform_name + ".mha", "w") as output_file:
      write_sequence_file_header(output_file, num_transforms)
      for i in range(num_transforms):
        write_sequence_file_transform(output_file, i, transform_name, transform_values[i])
      write_sequence_file_footer(output_file)

  
def write_sequence_file_header(f, num_transforms):
  f.write("ObjectType = Image" + "\n")
  f.write("NDims = 3" + "\n")
  f.write("AnatomicalOrientation = RAI" + "\n")
  f.write("BinaryData = True" + "\n")
  f.write("CompressedData = False" + "\n")
  f.write("DimSize = 0 0 " + str(num_transforms) + "\n")
  f.write("ElementSpacing = 1 1 1" + "\n")
  f.write("Offset = 0 0 0" + "\n")
  f.write("TransformMatrix = 1 0 0 0 1 0 0 0 1" + "\n")
  f.write("ElementType = MET_UCHAR" + "\n")
  f.write("Kinds = domain domain list" + "\n")

def write_sequence_file_transform(f, i, transform_name, transform_value):
  f.write("Seq_Frame" + str(i).rjust(4, "0") + "_" + transform_name + "ToTrackerTransform = " + transform_value[1] + "\n")
  f.write("Seq_Frame" + str(i).rjust(4, "0") + "_" + transform_name + "ToTrackerTransformStatus = OK" + "\n")
  f.write("Seq_Frame" + str(i).rjust(4, "0") + "_Timestamp = " + str(transform_value[0]) + "\n")

def write_sequence_file_footer(f):
  f.write("ElementDataFile = LOCAL" + "\n")

def get_entry_key_value(entry_string):
  entry_parts = entry_string.split(":")
  return entry_parts[0], entry_parts[1]

def leap_name_to_transform_name(leap_name):
  leap_name_parts = leap_name.split("_")
  if len(leap_name_parts) != 3:
    print("Could not parse joint name.")
    return None

  transform_name = ""
  transform_name = transform_name + HAND_MAP[leap_name_parts[0]]
  transform_name = transform_name + FINGER_MAP[leap_name_parts[1]]
  transform_name = transform_name + JOINT_MAP[leap_name_parts[2]]
  
  return transform_name

def position_string_to_transform_string(position_string):
  position_list = position_string.split(",")
  position_list = [x.strip() for x in position_list]

  transform_string = ""
  transform_string += "1 0 0 " + position_list[0] + " "
  transform_string += "0 1 0 " + position_list[1] + " "
  transform_string += "0 0 1 " + position_list[2] + " "
  transform_string += "0 0 0 1"

  return transform_string

if __name__ == "__main__":
  leap_filepath = sys.argv[1]

  leap_file_to_sequence_files(leap_filepath)