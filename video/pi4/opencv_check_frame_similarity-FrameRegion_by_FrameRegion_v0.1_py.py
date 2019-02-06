#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import measure
import os
import subprocess
import re



video_frames_path = '/media/2TB/datasets/traffic/video_frames/'
video_regions = 'regions/'
video_region_duplicates = 'regions/duplicates/'

camera = 'pi4/'
video_date = '2018-12-26_06-00'

regions_path = video_frames_path + camera + video_regions + video_date + "/"
regions_duplicates_path = video_frames_path + camera + video_region_duplicates + video_date + "/"

regions_path

regions_duplicates_path

#Create Region duplicate frames Directory
if not os.path.exists(regions_duplicates_path):
    os.mkdir(regions_duplicates_path)    
else:    
    print("Directory " + regions_duplicates_path +  " already exists")

os.chdir(regions_path)

print(os.getcwd())

list_of_file_names = video_date + '_region_files.txt'

if os.path.isfile(list_of_file_names):
    os.remove(list_of_file_names)

#execute shell command to list all files into a text file
log = open(list_of_file_names, 'a')
log.flush()  # <-- here's something not to forget!
proc = subprocess.Popen(['for f in *.jpg; do ls "$f"; done'], stdout=log, stderr=log, shell=True)

output = proc.communicate()[0] #waits for previous command to finish

file = open(list_of_file_names, 'r')

file_content = file.readlines()

file.close()

len(file_content)

file_content

def get_frame_number(fname):
    p0 = re.compile('frame_([0-9]?[0-9]?[0-9]?[0-9]?[0-9])')
    t0 = p0.search(fname.strip('\n'))
    
    p1= re.compile('([0-9]).jpg')
    t1 = p1.search(fname.strip('\n'))
    
    fnumber = t0.group(1)
    rnumber = t1.group(1)
    
    x = int(fnumber + rnumber)
    
    return x

file_content_sorted = []

for i in range(len(file_content)):
    file_content_sorted.append({"filename": file_content[i].strip('\n'), "frame_number": get_frame_number(file_content[i])})

file_content_sorted

# A function that returns the 'year' value:
def sorter(n):
  return n["frame_number"]

file_content_sorted.sort(key=sorter)

file_content_sorted



def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = measure.compare_ssim(imageA, imageB)
 
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
 
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the images
	plt.show()
	return s

for x in range(len(file_content_sorted)):
    similarity_score = 0
    img1_number = x
    img2_number = x + 2
    img1_name = file_content_sorted[img1_number]["filename"]
    img2_name = file_content_sorted[img2_number]["filename"]
    try:
        img1 = cv2.imread(img1_name,0)
        img2 = cv2.imread(img2_name,0)
        similarity_score = compare_images(img1,img2,"test")
        if similarity_score > 0.95:
            os.rename(regions_path+img2_name, regions_duplicates_path+img2_name)
        while similarity_score > 0.95:
            img2_number += 2
            img2_name = file_content_sorted[img2_number]["filename"]
            img2 = cv2.imread(img2_name,0)
            similarity_score = compare_images(img1,img2,"test")
            if similarity_score > 0.95:
                os.rename(regions_path+img2_name, regions_duplicates_path+img2_name)
    except:
        print("file moved")

