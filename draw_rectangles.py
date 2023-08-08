import os
import cv2

LOG_FILE = "image_log.txt"

def write_log(message):
    with open(LOG_FILE, 'a') as log:
        log.write(message + "\n")

def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt, img, clone

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)
        cv2.rectangle(clone, top_left_pt, bottom_right_pt, (0, 0, 255), 5)
        cv2.imshow('Draw Rectangle', clone)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = clone.copy()
            cv2.rectangle(temp_img, top_left_pt, (x, y), (0, 0, 255), 5)
            cv2.imshow('Draw Rectangle', temp_img)

if __name__ == '__main__':
    global drawing, top_left_pt, bottom_right_pt, img, clone

    input_folder = "Images"

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as log:
            pass

    print("Keys: [d] - Delete, [s] - Save, [i] - Ignore, [q] - Quit")

    screen_width, screen_height = 1920, 1080

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                input_path = os.path.join(root, filename)

                with open(LOG_FILE, 'r') as log:
                    if input_path in log.read():
                        continue

                img = cv2.imread(input_path)
                h, w = img.shape[:2]

                aspect_ratio = w / h
                new_width = int(screen_height * aspect_ratio)
                new_height = screen_height

                if new_width > screen_width:
                    new_width = screen_width
                    new_height = int(screen_width / aspect_ratio)

                scale_x = w / new_width
                scale_y = h / new_height

                clone = cv2.resize(img, (new_width, new_height))
                drawing = False
                top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

                cv2.namedWindow('Draw Rectangle', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Draw Rectangle', new_width, new_height)
                cv2.setMouseCallback('Draw Rectangle', draw_rectangle)

                while True:
                    cv2.imshow('Draw Rectangle', clone)
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("d"):
                        os.remove(input_path)
                        write_log(f"Deleted: {input_path}")
                        print(f"Deleted: {input_path}")
                        break

                    elif key == ord("s"):
                        if top_left_pt != (-1, -1) and bottom_right_pt != (-1, -1):
                            x1, y1 = int(top_left_pt[0] * scale_x), int(top_left_pt[1] * scale_y)
                            x2, y2 = int(bottom_right_pt[0] * scale_x), int(bottom_right_pt[1] * scale_y)

                            cropped_img = img[y1:y2, x1:x2]
                            cv2.imwrite(input_path, cropped_img)
                            write_log(f"Cropped and saved: {input_path}")
                            print(f"Cropped and saved: {input_path}")
                        break

                    elif key == ord("i"):
                        write_log(f"Ignored: {input_path}")
                        print(f"Ignored: {input_path}")
                        break

                    elif key == ord("q"):
                        cv2.destroyAllWindows()
                        exit(0)

                cv2.destroyWindow('Draw Rectangle')
                continue
