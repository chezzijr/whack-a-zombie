import pygame

class Animation:
    def __init__(self, frames: list[pygame.Surface], repeat: bool = True):
        self.frames = frames
        self.current_frame = 0
        self.frame_count = len(frames)
        self.repeat = repeat

    # only return None if the animation is not repeating and reached the end
    def next_frame(self, flip=False) -> pygame.Surface | None:
        frame = self.frames[self.current_frame]
        self.current_frame += 1
        if self.current_frame == self.frame_count:
            if self.repeat:
                self.current_frame = 0
            else:
                return None
        return frame if not flip else pygame.transform.flip(frame, True, False)

    def reset(self) -> None:
        self.current_frame = 0
