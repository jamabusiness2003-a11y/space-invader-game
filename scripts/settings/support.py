from .imports import *

def aspect_ratio(target_width, target_height, img, img_size):
    width, height = img_size

    scaled_width = target_width / width
    scaled_height = target_height / height

    scale_factor = min(scaled_width, scaled_height)

    new_width = width * scale_factor
    new_height = height * scale_factor

    img = pygame.transform.smoothscale(img, (new_width, new_height))

    return img

def import_frames(*path):
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
    return audio_dict