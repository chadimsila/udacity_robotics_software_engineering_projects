# Import PCL module
import pcl
import numpy as np
import matplotlib.pyplot as plt
# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')
            # Voxel Grid filter
# Create a VoxelGrid filter object for our input point cloud
vox = cloud.make_voxel_grid_filter()  
# Choose a voxel (also known as leaf) size
# Note: this (1) is a poor choice of leaf size   
# Experiment and find the appropriate size!
LEAF_SIZE = 0.01  

# Set the voxel (or leaf) size  
vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

# Call the filter function to obtain the resultant downsampled point cloud
cloud_filtered = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filtered, filename)

            # PassThrough filter

passthrough = cloud_filtered.make_passthrough_filter()
passthrough.set_filter_field_name("z")
passthrough.set_filter_limits(0.1, 0.8)
# //pass.setFilterLimitsNegative (true)
cloud_filtered2 = passthrough.filter()
filename = 'passthrough_downsampled.pcd'
pcl.save(cloud_filtered2, filename)



# RANSAC plane segmentation
# Create the segmentation object
seg = cloud_filtered2.make_segmenter()

# Set the model you wish to fit 
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)

# Max distance for a point to be considered fitting the model
# Experiment with different values for max_distance 
# for segmenting the table
max_distance = 1
seg.set_distance_threshold(max_distance)

# Call the segment function to obtain set of inlier indices and model coefficients
inliers, coefficients = seg.segment()

# Extract inliers
extracted_inliers = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliers.pcd'
pcl.save(extracted_inliers, filename)


extracted_outliers = cloud_filtered.extract(inliers, negative=True)
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)

# Extract outliers


# Save pcd for tabletop objects

