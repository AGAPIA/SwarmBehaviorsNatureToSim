from PIL import Image
from os import listdir

import torchvision.transforms.functional as fct

image_names = sorted(listdir('./customdata/images'))
print(image_names)

img_array = []

for img_name in image_names:
    full_image_path = "./customdata/images/{}".format(img_name)
    img = Image.open(full_image_path)
    img = fct.to_tensor(img)
    img = img[:3, :, :]
    img_array.append(img)


def retrieve_image_from_coordinate(x, y):
    batch_num = -1
    subset_num = -1

    if 150 <= y < 260:
        subset_num = 0
    elif 50 <= y < 150:
        subset_num = 1
    elif -50 <= y < 50:
        subset_num = 2
    else:
        subset_num = 3

    if -250 <= x < -125:
        batch_num = 0
    elif -125 <= x < -50:
        batch_num = 1
    elif -50 <= x < 50:
        batch_num = 2
    elif 50 <= x < 100:
        batch_num = 3
    elif 100 <= x <= 150:
        batch_num = 4
    elif 150 <= x < 250:
        batch_num = 5

    img_num = 4 * batch_num + subset_num

    return img_array[img_num]


temp_img = retrieve_image_from_coordinate(img_array, -72, -150)
#im = fct.to_pil_image(temp_img)

#im.show()
