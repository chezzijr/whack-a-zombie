import pygame

class Animation:
    def __init__(self, frames: list[pygame.Surface], repeat: bool = True):
        if not frames:
            raise ValueError("No frames provided")
        self.frames = frames
        self.current_frame = 0
        self.frame_count = len(frames)
        self.repeat = repeat

    def get_first_frame(self) -> pygame.Surface:
        return self.frames[0]

    # only return None if the animation is not repeating and reached the end
    def next_frame(self, flip=False) -> pygame.Surface | None:
        if self.is_ended() and not self.repeat:
            return None
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % self.frame_count if self.repeat else self.current_frame + 1
        return frame if not flip else pygame.transform.flip(frame, True, False)

    def is_ended(self) -> bool:
        return self.current_frame == self.frame_count

    def reset(self) -> None:
        self.current_frame = 0
