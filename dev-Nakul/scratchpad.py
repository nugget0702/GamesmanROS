import numpy as np
from scipy.spatial.transform import Rotation as R

# Quaternion for +180 degrees rotation around Z-axis
q_z = R.from_quat([0, 0, 0, 1])

# Quaternion for 180 degrees rotation around X-axis
q_x = R.from_quat([0, 1, 0, 0])

# Combine the rotations
combined_q = q_x * q_z

# Output the combined quaternion
combined_quaternion = combined_q.as_quat()
print("Combined Quaternion:", combined_quaternion)
