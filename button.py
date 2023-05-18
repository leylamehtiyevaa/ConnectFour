import pygame

pygame.init()

class Button:
    def __init__(self, text, position, size, color, hover_color, text_color, action):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        rect = pygame.Rect(self.position, self.size)
        pygame.draw.rect(surface, self.color, rect)

        font = pygame.font.Font(None, 30)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and \
                    self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]:
                self.action()




pygame.quit()
