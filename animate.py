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

# so that animations can be played at any frame rate
class TimeAnimation(Animation):
    def __init__(self, frames: list[pygame.Surface], frame_duration: float, repeat: bool = True):
        super().__init__(frames, repeat)
        self.frame_duration = frame_duration
        self.elapsed_time = 0
        self.curr_frame = super().get_first_frame()

    def next_frame_with_dt(self, dt: float, flip: bool = False) -> pygame.Surface | None:
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time -= self.frame_duration
            self.curr_frame = super().next_frame(flip)
        return self.curr_frame

    def reset(self) -> None:
        self.elapsed_time = 0
        super().reset()
