import matplotlib.pyplot as plt
import numpy as np
import sys

def read_sequence_positions(sequence_filepath, transform_name):
  translation_array = np.empty((0, 3))
  time_array = np.empty((0, 1))

  with open(sequence_filepath, "r") as sequence_file:
    for line in sequence_file:
      split_line = line.replace("=", " ").split()
      field_name = split_line[0]
      field_value = split_line[1:]

      if transform_name in field_name and "Status" not in field_name and "Matrix" not in field_name:
        curr_translation = np.hstack((float(field_value[3]), float(field_value[7]), float(field_value[11])))
        translation_array = np.vstack((translation_array, curr_translation))

      elif "Timestamp" in field_name:
        curr_timestamp = float(field_value[0])
        time_array = np.vstack((time_array, curr_timestamp))

    return time_array, translation_array


def plot_sequence_positions(time_array, translation_array):
  fig = plt.figure()

  plt.subplot(3, 1, 1)
  plt.plot(time_array, translation_array[:, 0], marker="")

  plt.subplot(3, 1, 2)
  plt.plot(time_array, translation_array[:, 1], marker="")

  plt.subplot(3, 1, 3)
  plt.plot(time_array, translation_array[:, 2], marker="")

  plt.show(block=False)


if __name__ == "__main__":
  for i in range(1, len(sys.argv)):
    time_array, translation_array = read_sequence_positions(sys.argv[i], "Transform")
    plot_sequence_positions(time_array, translation_array)

  plt.show()