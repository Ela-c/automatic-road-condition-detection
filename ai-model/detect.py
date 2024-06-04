import sys
import time
import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import requests
from utils import visualize, request_location
from persistance import insert_record
from asyncio import run


def runDetection(model: str, width: int, height: int) -> None:
    """Continuously run inference on images

    Args:
      model: Name of the TFLite object detection model.
      width: The width of the frame captured from the camera.
      height: The height of the frame captured from the camera.
    """
    another_counter = 1
    period = time.time()
    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture("http://raspberrypi.local:5000/video_feed")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    detection_result_list = []

    def visualize_callback(result: vision.ObjectDetectorResult,
                           output_image: mp.Image, timestamp_ms: int):
        result.timestamp_ms = timestamp_ms
        detection_result_list.append(result)

    # Initialize the object detection model
    base_options = python.BaseOptions(model_asset_path=model)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                           running_mode=vision.RunningMode.LIVE_STREAM,
                                           score_threshold=0.5,
                                           result_callback=visualize_callback)
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        # Run object detection using the model.
        detector.detect_async(mp_image, counter)
        current_frame = mp_image.numpy_view()
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2BGR)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        if detection_result_list:
            print(detection_result_list)
            vis_image = visualize(current_frame, detection_result_list[0])
            cv2.imshow('object_detector', vis_image)
            # add point to the database
            if (time.time() - period) > 10:
                period = time.time()
                try:
                    run(insert_record_wrapper(another_counter))
                    run(save_image(vis_image, another_counter))
                except Exception as e:
                    print(f"Error during database insert or save image: {e}")
                another_counter += 1
            detection_result_list.clear()
        else:
            cv2.imshow('object_detector', current_frame)

        # time.sleep(1)
        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break

    detector.close()
    cap.release()
    cv2.destroyAllWindows()


async def insert_record_wrapper(id):
    try:
        image_url = f'images/{id}.jpg'
        location = request_location(
            "http://raspberrypi.local:5000/location")
        lat = location['lat']
        long = location['long']
        insert_record("", lat, long, image_url)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")
    except Exception as e:
        print(f"An error occurred in insert_record_wrapper: {e}")


async def save_image(image, img_counter):
    # Save with leading zeros for better sorting
    filename = f'images/{img_counter}.jpg'
    cv2.imwrite(filename, image)
    print(f'Saved {filename}')


runDetection('model.tflite', 1280, 720)
