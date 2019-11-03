# from moviepy.editor import VideoFileClip
from svm_pipeline import *
from yolo_pipeline import *
from lane import *
from PIL import Image, ImageOps
from resizeimage import resizeimage
import os

num_skipped=0
total_processed=0

def pipeline_yolo(img):

    # img_undist, img_lane_augmented, lane_info = lane_process(img)
    output = vehicle_detection_yolo(img)

    return output

def pipeline_svm(img):

    img_undist, img_lane_augmented, lane_info = lane_process(img)
    output = vehicle_detection_svm(img_undist, img_lane_augmented, lane_info)

    return output


if __name__ == "__main__":

    demo = 1  # 1:image (YOLO and SVM), 2: video (YOLO Pipeline), 3: video (SVM pipeline)
    
    img_folder_name='img'
    output_image_folder_name = 'output_img'

    folders=os.listdir('./'+img_folder_name)
    
    num_images=0
    
    input_image_path=[]
    output_image_path=[]

    for folder in folders:
        images_in_folder = os.listdir('./'+img_folder_name+'/'+folder)
        for image in images_in_folder:
            input_image_path = img_folder_name + '/'+folder+'/'+image
            output_image_path=  output_image_folder_name + '/'+folder+'/'+image
            num_images +=1

            print(input_image_path)
            with open(input_image_path, 'r+b') as f:
                with Image.open(f) as image:

                    size = (1280, 720)
                    fit_and_resized_image = ImageOps.fit(image, size, Image.ANTIALIAS)
                    # cover = resizeimage.resize_cover(image, [1280, 720])
                    fit_and_resized_image.save(input_image_path, image.format)


            if demo == 1:
                filename = input_image_path
                image = mpimg.imread(filename)

                yolo_result = pipeline_yolo(image)
                cv2.imwrite(output_image_path, yolo_result)

                # # s(2) SVM pipeline
                # draws_img = pipeline_svm(image)
                # fig = plt.figure()
                # plt.imshow(draws_img)
                # plt.title('svm pipeline', fontsize=30)
                # plt.show()

            elif demo == 2:
                # YOLO Pipeline
                video_output = 'examples/project_YOLO.mp4'
                clip1 = VideoFileClip("examples/project_video.mp4").subclip(30,32)
                clip = clip1.fl_image(pipeline_yolo)
                clip.write_videofile(video_output, audio=False)

            else:
                # SVM pipeline
                video_output = 'examples/project_svm.mp4'
                clip1 = VideoFileClip("examples/project_video.mp4").subclip(30,32)
                clip = clip1.fl_image(pipeline_svm)
                clip.write_videofile(video_output, audio=False)

    print(num_images)


