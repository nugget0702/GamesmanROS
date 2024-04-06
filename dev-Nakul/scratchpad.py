import numpy as np
from scipy.spatial.transform import Rotation as R

# Quaternion for 90 degrees rotation around Z-axis
q_z = R.from_quat([0, 0, np.sqrt(2)/2, np.sqrt(2)/2])

# Quaternion for 180 degrees rotation around Y-axis (to simulate flipping X after rotation)
q_y_flip = R.from_quat([0, 1, 0, 0])

# Combine the rotations
combined_q = q_y_flip * q_z

# Output the combined quaternion
combined_quaternion = combined_q.as_quat()
print("Combined Quaternion:", combined_quaternion)
