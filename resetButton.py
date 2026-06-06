import pygame

#reset button
BUTTON_WIDTH = 210
BUTTON_HEIGHT = 42
BUTTON_MARGIN_X = 20
BUTTON_MARGIN_Y = 800


def get_reset_button_rect(screen):
    return pygame.Rect(
        screen.get_width() - BUTTON_WIDTH - BUTTON_MARGIN_X,
        BUTTON_MARGIN_Y,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )


def draw_reset_button(screen, mouse_position):
    reset_button_shape = get_reset_button_rect(screen)

    is_hovering_reset = reset_button_shape.collidepoint(mouse_position)

    button_font = pygame.font.SysFont("bahnschrift", 18, bold=True)

    # NASA-inspired mission-control button styling.
    base_color = (25, 33, 42) if is_hovering_reset else (18, 25, 34)
    frame_color = (90, 130, 160) if is_hovering_reset else (70, 105, 130)
    accent_color = (0, 210, 255) if is_hovering_reset else (0, 165, 215)
    text_color = (245, 250, 255)

    pygame.draw.rect(screen, base_color, reset_button_shape, border_radius=4)
    pygame.draw.rect(screen, frame_color, reset_button_shape, 2, border_radius=4)

    # Corner accents emulate instrument panel framing.
    x, y, w, h = reset_button_shape
    corner_len = 12
    pygame.draw.line(screen, accent_color, (x + 1, y + 1), (x + 1 + corner_len, y + 1), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + 1), (x + 1, y + 1 + corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + 1), (x + w - 2 - corner_len, y + 1), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + 1), (x + w - 2, y + 1 + corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + h - 2), (x + 1 + corner_len, y + h - 2), 2)
    pygame.draw.line(screen, accent_color, (x + 1, y + h - 2), (x + 1, y + h - 2 - corner_len), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + h - 2), (x + w - 2 - corner_len, y + h - 2), 2)
    pygame.draw.line(screen, accent_color, (x + w - 2, y + h - 2), (x + w - 2, y + h - 2 - corner_len), 2)

    # Small status indicator for a cockpit-style visual cue.
    indicator_color = (72, 255, 110) if is_hovering_reset else (200, 95, 70)
    pygame.draw.circle(screen, indicator_color, (x + 14, y + h // 2), 5)

    reset_button_text = button_font.render("RESET ZOOM", True, text_color)
    text_rect = reset_button_text.get_rect(center=reset_button_shape.center)
    text_rect.x += 8

    screen.blit(reset_button_text, text_rect)