#v1.1: changed time_region = np.array([745,604]) to time_region = np.array([747,604]) as some extra pixels where 
#      showing up on the left causing the OCR to give incorrect results
#v1.2: time region to extract: time_region_size_h = 24, time_region = np.array([747,600])
#      added loop for OCR of time
#      added default time if still unrecognized
#      added os create directories

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os

#Videos to split
videos = [
#'vokoscreen-2019-01-09_15-30-00.mp4',
'vokoscreen-2019-01-09_06-00-00.mp4',
'vokoscreen-2019-01-05_06-00-00.mp4',
'vokoscreen-2019-01-06_06-00-01.mp4'
]

video_frames = '/media/2TB/datasets/traffic/video_frames/pi4/fullframe/'
video_regions = '/media/2TB/datasets/traffic/video_frames/pi4/regions/'
video_path = '/media/2TB/datasets/traffic/video_frames/pi4/video/'

#Set variables
video_no = 0

#select regions to extract (Camera 0)
#image size = 954x624
region_size_h = 240
region_size_w = 240

#regions to select, [x,y] coordinates of top left hand corner
regions = np.array([[583,170]])
number_of_regions = regions[0:,:1].size

#time region to extract
time_region_size_h = 24
time_region_size_w = 55
#time_region = np.array([742,600])
time_region = np.array([745,600])

#Write full frame image to file, and individual frame regions; in each case add the time to the file name
while video_no < len(videos):
    frame_no = 0
    video_name = videos[video_no]
    my_video_name = video_name.split(".")[0]
    vidcap = cv2.VideoCapture(video_path+video_name)
    video_date = videos[video_no][11:27]

    #write to log
    text_file_name = video_date+"_output.txt"
    text_file = open(text_file_name, "w")
    
    #Create Full frames Directory
    if not os.path.exists(video_frames+video_date):
        os.mkdir(video_frames+video_date)
        text_file.write("Directory " + video_frames+video_date +  " created" +"\n")
    else:    
        text_file.write("Directory " + video_frames+video_date +  " already exists" +"\n")
 
    #Create Region frames Directory
    if not os.path.exists(video_regions+video_date):
        os.mkdir(video_regions+video_date)
        text_file.write("Directory " + video_regions+video_date +  " created" +"\n")    
    else:    
        text_file.write("Directory " + video_regions+video_date +  " already exists" +"\n")
            
    TOTAL_FRAMES_FLAG = cv2.CAP_PROP_FRAME_COUNT
    num_frames = vidcap.get(TOTAL_FRAMES_FLAG)

    while frame_no < num_frames:
        vidcap.set(1, frame_no)
        success,image = vidcap.read()

        #extract time region from frame, and convert to string
        time_img_region = image[time_region[1]:time_region[1]+time_region_size_h, time_region[0]:time_region[0]+time_region_size_w]

        #set variables to loop tille time is recognized as a numeric value, and set limit on how much to try
        time = 'na'
        resize_ratio = 2
        GaussianBlur_value = 1
        last_resize_ratio = 15

        while not time.isnumeric() and resize_ratio <= last_resize_ratio:
            #convert time_img_region to greyscale; then increase six=ze and blur to make readable for OCR
            grey = cv2.cvtColor(time_img_region, cv2.COLOR_BGR2GRAY)
            grey = cv2.resize(grey, None, fx=resize_ratio, fy=resize_ratio, interpolation=cv2.INTER_AREA)

            for g in range(GaussianBlur_value,GaussianBlur_value+10,2):
                if not time.isnumeric():
                    grey = cv2.GaussianBlur(grey,(g,g),0)
                    grey = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

                    #write the grayscale image to disk as a temporary file so that OCR can be applied to it
                    filename = "{}.png".format(os.getpid())
                    cv2.imwrite(filename, grey)

                    #load the image, apply OCR, and then delete the temporary file
                    time = pytesseract.image_to_string(Image.open(filename))
                    time = time.replace(':','')

                    #for cases where OCR appends a comma (when last digit is 1 for example), exclude the comma
                    time = time[:5]
                else:
                    break
            resize_ratio += 1
            GaussianBlur_value += 2
        
        #delete temporary file
        os.remove(filename)
        
        #if time has not been resolved as numeric, set default 0000
        if not time.isnumeric():
            time = '9999'

        if  (int(time) > 930 and int(time) < 1500) or int(time) > 1835 or int(time) < 559:
            time = '9999'
            
            
        #store the frame
        cv2.imwrite(video_frames+video_date+"/"+my_video_name+"_"+time+"_frame_%d.jpg" % frame_no, image)
        text_file.write(my_video_name+"_"+time+"_frame%d.jpg" % frame_no +"\n")

        #store the frame regions
        region_no = 0
        while region_no < number_of_regions:
            img_region = image[regions[region_no,1]:regions[region_no,1]+region_size_h, regions[region_no,0]:regions[region_no,0]+region_size_w]
            cv2.imwrite(video_regions+video_date+"/"+my_video_name+"_"+time+"_frame_%d" % frame_no+"_%d.jpg" % region_no, img_region)
            text_file.writelines(my_video_name+"_"+time+"_frame%d" % frame_no+"_%d.jpg" % region_no +"\n")
            region_no += 1
        frame_no += 1
    video_no += 1
