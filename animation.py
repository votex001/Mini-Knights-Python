import pygame

class Animation:
    def __init__(self, path = 'character/animations', imgs_map = None, frame_duration=50,SCALE_FACTOR = 1):

        self.SCALE_FACTOR = SCALE_FACTOR




        self.path = path
        self.map = imgs_map
        self.cashed_frames = {}
        self.last_update_times = {}
        self.frame_duration = frame_duration
        self.animation_indices = {}

        self.load("idle")

    def scale_img(self,img,lookSide ="right"):
        width, height = img.get_size()
        new_size = (int(width * self.SCALE_FACTOR), int(height * self.SCALE_FACTOR))
        new_img = pygame.transform.scale(img, new_size)
        if lookSide == "left": 
            new_img = pygame.transform.flip(new_img,True,False)
        return new_img

    def load(self, animation_name, lookSide="right"):
        if not self.map:
            return []

        total_imgs, rect_frame_num = self.map[animation_name]

        cache_key = (animation_name, lookSide)
        if cache_key in self.cashed_frames:
            return self.cashed_frames[cache_key]

        frames = []
        for i in range(total_imgs):
            frame = self.scale_img(pygame.image.load(f'{self.path}/{animation_name}/{i+1}.png').convert_alpha(), lookSide)
            frames.append(frame)

        rect_frame = frames[rect_frame_num-1] 
        self.cashed_frames[cache_key] = (frames, rect_frame)

        return frames, rect_frame
        
    def reset_animation(self, animation_name):
        self.animation_indices[animation_name] = 0
        self.last_update_times[animation_name] = pygame.time.get_ticks()


    def next_frame(self, animation_name, lookSide="right",once = False):
        frames, rect_frame = self.load(animation_name, lookSide)
        if not frames:
            return None

        now = pygame.time.get_ticks()

        if animation_name not in self.animation_indices:
            self.animation_indices[animation_name] = 0
            self.last_update_times[animation_name] = now
   
        current_index = self.animation_indices[animation_name]
        is_last_frame = False

        if now - self.last_update_times[animation_name] >= self.frame_duration:
            next_index = (current_index + 1) % len(frames)
            self.animation_indices[animation_name] = next_index
            self.last_update_times[animation_name] = now

            if next_index == 0:
                is_last_frame = True
            prev_index = current_index
            current_index = next_index
            if next_index == 0 and once:
                current_index = prev_index
                self.animation_indices[animation_name] = prev_index

        return frames[current_index], rect_frame, is_last_frame

