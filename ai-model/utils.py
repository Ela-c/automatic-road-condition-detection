import cv2
import numpy as np
import requests
import base64

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def request_location(url):

    payload = {'address':  base64.b64encode(
        "463 Elizabeth St, Melbourne VIC".encode("ascii"))}
    response = requests.get(url, params=payload)
    return response.json()


def visualize(
    image,
    detection_result
) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Args:
      image: The input RGB image.
      detection_result: The list of all "Detection" entities to be visualized.
    Returns:
      Image with bounding boxes.
    """
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        # Draw label and score
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x,
                         MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image


def stream_images_from_url(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        byte_stream = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            byte_stream += chunk
            a = byte_stream.find(b'\xff\xd8')
            b = byte_stream.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = byte_stream[a:b+2]
                byte_stream = byte_stream[b+2:]
                image = cv2.imdecode(np.frombuffer(
                    jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # save_image(image, img_counter)
    else:
        print(
            f"Failed to connect to {url}. Status code: {response.status_code}")
