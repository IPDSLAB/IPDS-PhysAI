import gphoto2 as gp
import time
import os

camera = gp.Camera()
camera.init()

#save_dir = "stack_images_"
save_dir = "stiching_images_demo7"
os.makedirs(save_dir, exist_ok=True)

steps = [
    "Far 3",
    "Far 2",
    "Far 1",
    "Near 1",
    "Near 2",
    "Near 3"
]

img_index = 0

#for i in range(5):
for i in range(1):

    for step in steps:

        print("focus:", step)

        # 포커스 이동
        config = camera.get_config()
        focus = config.get_child_by_name("manualfocusdrive")

        focus.set_value(step)
        camera.set_config(config)

        time.sleep(0.5)

        # 촬영
        file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

        camera_file = camera.file_get(
            file_path.folder,
            file_path.name,
            gp.GP_FILE_TYPE_NORMAL
        )

        # 👉 파일명에 focus 정보 포함
        save_path = os.path.join(
            save_dir,
            f"{img_index:03d}_{step.replace(' ', '')}.jpg"
        )

        camera_file.save(save_path)

        print("saved:", save_path)

        img_index += 1

        time.sleep(1.5)

camera.exit()
