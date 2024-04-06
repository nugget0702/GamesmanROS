import numpy as np
from scipy.spatial.transform import Rotation as R

# Quaternion for -90 degree rotation around X-axis
qx = R.from_euler('x', -90, degrees=True)

# Quaternion for -90 degree rotation around Y-axis
qy = R.from_euler('y', -90, degrees=True)

# Combined rotation: first around X, then around Y
q_combined = qy * qx

# Convert to quaternion (x, y, z, w) format
combined_quat = q_combined.as_quat()

print("Combined rotation quaternion:", combined_quat)
