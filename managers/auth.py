import pygame
import math
import random

from db import create_player, login_player, username_exists


class AuthUI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont("consolas", 42, bold=True)
        self.section_font = pygame.font.SysFont("consolas", 26, bold=True)
        self.label_font = pygame.font.SysFont("consolas", 14, bold=True)
        self.input_font = pygame.font.SysFont("consolas", 17)
        self.button_font = pygame.font.SysFont("consolas", 18, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 12, bold=True)
        self.error_font = pygame.font.SysFont("consolas", 13, bold=True)

        self.bg = (7, 2, 14)
        self.panel = (19, 5, 25)

        self.pink = (255, 45, 180)
        self.light_pink = (255, 130, 225)
        self.bright_pink = (255, 215, 250)

        self.white = (255, 245, 255)
        self.gray = (180, 155, 180)

        self.grid_color = (75, 12, 70)
        self.deep_pink = (100, 15, 90)

        self.error_color = (255, 80, 105)

        self.username = ""
        self.password = ""
        self.confirm_password = ""

        self.active_field = "username"

        self.show_password = False
        self.show_confirm = False

        self.error_msg = ""

        self.mode = "menu"

        self.current_user = None

        self.cursor_timer = 0

        cx = screen_width // 2

        input_w = 390
        input_h = 46

        self.username_rect = pygame.Rect(
            cx - input_w // 2,
            245,
            input_w,
            input_h
        )

        self.password_rect = pygame.Rect(
            cx - input_w // 2,
            315,
            input_w,
            input_h
        )

        self.confirm_rect = pygame.Rect(
            cx - input_w // 2,
            385,
            input_w,
            input_h
        )

        eye_size = 24

        self.pass_eye_rect = pygame.Rect(
            self.password_rect.right - 34,
            self.password_rect.y + 11,
            eye_size,
            eye_size
        )

        self.confirm_eye_rect = pygame.Rect(
            self.confirm_rect.right - 34,
            self.confirm_rect.y + 11,
            eye_size,
            eye_size
        )

        self.button_w = 170
        self.button_h = 48
        self.button_gap = 20

        self.action_y = 455

        self.back_btn_rect = pygame.Rect(
            cx - self.button_w - self.button_gap // 2,
            self.action_y,
            self.button_w,
            self.button_h
        )

        self.submit_btn_rect = pygame.Rect(
            cx + self.button_gap // 2,
            self.action_y,
            self.button_w,
            self.button_h
        )

        self.login_btn_rect = pygame.Rect(
            cx - 205 - 12,
            235,
            205,
            52
        )

        self.signup_btn_rect = pygame.Rect(
            cx + 12,
            235,
            205,
            52
        )

        self.forgot_pass_rect = pygame.Rect(
            self.password_rect.right - 165,
            self.password_rect.bottom + 6,
            165,
            20
        )

        self.help_center_rect = pygame.Rect(
            cx - 110,
            screen_height - 35,
            220,
            22
        )

        random.seed(7)

        self.stars = [
            (
                random.randint(20, screen_width - 20),
                random.randint(55, screen_height - 90),
                random.choice([1, 1, 1, 2])
            )
            for _ in range(65)
        ]

    def set_mode(self, mode):
        self.mode = mode
        self.reset_fields()

    def reset_fields(self):
        self.username = ""
        self.password = ""
        self.confirm_password = ""
        self.active_field = "username"
        self.show_password = False
        self.show_confirm = False
        self.error_msg = ""
        self.cursor_timer = 0

    def update(self):
        self.cursor_timer += 1

        if self.cursor_timer >= 60:
            self.cursor_timer = 0

    def submit(self, mode):
        username = self.username.strip()
        password = self.password.strip()

        if not username or not password:
            self.error_msg = "FIELDS CANNOT BE EMPTY"
            return False

        if len(username) < 3:
            self.error_msg = "USERNAME TOO SHORT"
            return False

        if mode == "login":
            player = login_player(username, password)

            if player is None:
                self.error_msg = "INVALID USERNAME OR PASSWORD"
                return False

            self.current_user = {
                "player_id": player["player_id"],
                "username": player["username"]
            }

            self.error_msg = ""

            return True

        confirm = self.confirm_password.strip()

        if not confirm:
            self.error_msg = "FIELDS CANNOT BE EMPTY"
            return False

        if password != confirm:
            self.error_msg = "PASSWORDS DO NOT MATCH"
            return False

        if username_exists(username):
            self.error_msg = "USERNAME ALREADY EXISTS"
            return False

        player_id = create_player(
            username,
            password
        )

        if player_id is None:
            self.error_msg = "DATABASE ERROR"
            return False

        self.current_user = {
            "player_id": player_id,
            "username": username
        }

        self.error_msg = ""

        return True

    def draw_neon_rect(self, screen, rect, color, width=2):
        pygame.draw.rect(
            screen,
            (55, 7, 48),
            rect.inflate(10, 10),
            1,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (100, 12, 82),
            rect.inflate(6, 6),
            1,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            color,
            rect,
            width,
            border_radius=5
        )

    def draw_stars(self, screen):
        for x, y, size in self.stars:
            pygame.draw.circle(
                screen,
                self.light_pink,
                (x, y),
                size
            )

    def draw_planet(self, screen):
        cx = self.screen_width // 2
        cy = self.screen_height + 75
        radius = 145

        for r in range(radius, 0, -5):
            ratio = r / radius

            color = (
                int(55 * ratio + 20),
                int(7 * ratio),
                int(50 * ratio + 15)
            )

            pygame.draw.circle(
                screen,
                color,
                (cx, cy),
                r
            )

        pygame.draw.arc(
            screen,
            self.light_pink,
            (
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2
            ),
            math.pi,
            math.pi * 2,
            2
        )

        pygame.draw.arc(
            screen,
            self.pink,
            (
                cx - radius + 8,
                cy - radius + 8,
                (radius - 8) * 2,
                (radius - 8) * 2
            ),
            math.pi,
            math.pi * 2,
            1
        )

    def draw_wireframe_floor(self, screen):
        horizon = int(self.screen_height * 0.80)

        for row in range(9):
            y = horizon + row * 18

            pygame.draw.line(
                screen,
                self.grid_color,
                (0, y),
                (self.screen_width, y),
                1
            )

        center_x = self.screen_width // 2

        for x in range(
            -self.screen_width,
            self.screen_width * 2,
            40
        ):
            pygame.draw.line(
                screen,
                self.grid_color,
                (center_x, horizon),
                (x, self.screen_height),
                1
            )

    def draw_spaceship(self, screen, x, y, scale=1.0, bright=True):
        color = self.bright_pink if bright else self.light_pink

        outer = [
            (x, y - int(24 * scale)),
            (x - int(10 * scale), y - int(5 * scale)),
            (x - int(29 * scale), y + int(11 * scale)),
            (x - int(13 * scale), y + int(10 * scale)),
            (x - int(7 * scale), y + int(24 * scale)),
            (x, y + int(17 * scale)),
            (x + int(7 * scale), y + int(24 * scale)),
            (x + int(13 * scale), y + int(10 * scale)),
            (x + int(29 * scale), y + int(11 * scale)),
            (x + int(10 * scale), y - int(5 * scale))
        ]

        pygame.draw.polygon(
            screen,
            (30, 3, 30),
            outer
        )

        pygame.draw.lines(
            screen,
            color,
            True,
            outer,
            2
        )

        cockpit = [
            (x, y - int(15 * scale)),
            (x - int(6 * scale), y + int(6 * scale)),
            (x + int(6 * scale), y + int(6 * scale))
        ]

        pygame.draw.polygon(
            screen,
            self.pink,
            cockpit
        )

        flame = [
            (x - int(6 * scale), y + int(19 * scale)),
            (x, y + int(37 * scale)),
            (x + int(6 * scale), y + int(19 * scale))
        ]

        pygame.draw.polygon(
            screen,
            self.bright_pink,
            flame
        )

    def draw_side_ship(self, screen, x, y, scale=1.0, direction=1):
        points = [
            (x, y),
            (
                x + int(35 * scale) * direction,
                y - int(12 * scale)
            ),
            (
                x + int(58 * scale) * direction,
                y
            ),
            (
                x + int(35 * scale) * direction,
                y + int(12 * scale)
            )
        ]

        pygame.draw.polygon(
            screen,
            (25, 3, 28),
            points
        )

        pygame.draw.lines(
            screen,
            self.pink,
            True,
            points,
            2
        )

        pygame.draw.line(
            screen,
            self.light_pink,
            (
                x + int(58 * scale) * direction,
                y
            ),
            (
                x + int(80 * scale) * direction,
                y
            ),
            2
        )

    def draw_asteroid(self, screen, x, y, radius):
        points = []

        for i in range(9):
            angle = math.pi * 2 * i / 9
            variation = 0.75 + ((i * 13) % 6) / 10

            px = x + math.cos(angle) * radius * variation
            py = y + math.sin(angle) * radius * variation

            points.append((int(px), int(py)))

        pygame.draw.polygon(
            screen,
            (18, 3, 22),
            points
        )

        pygame.draw.lines(
            screen,
            self.deep_pink,
            True,
            points,
            1
        )

    def draw_hud(self, screen):
        for i in range(3):
            x = 35 + i * 34
            y = 32

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x, y + 3, 7, 7)
            )

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x + 8, y + 3, 7, 7)
            )

            pygame.draw.rect(
                screen,
                self.light_pink,
                (x + 4, y + 10, 8, 7)
            )

        unlimited = self.small_font.render(
            "UNLIMITED",
            True,
            self.light_pink
        )

        screen.blit(
            unlimited,
            (154, 35)
        )

        bx = self.screen_width - 72
        by = 32

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx, by, 39, 17),
            2
        )

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx + 39, by + 5, 4, 7)
        )

        pygame.draw.rect(
            screen,
            self.light_pink,
            (bx + 5, by + 4, 12, 9)
        )

    def draw_background(self, screen):
        screen.fill(self.bg)

        inner = pygame.Rect(
            17,
            17,
            self.screen_width - 34,
            self.screen_height - 34
        )

        pygame.draw.rect(
            screen,
            (11, 2, 17),
            inner
        )

        self.draw_stars(screen)

        self.draw_asteroid(
            screen,
            65,
            250,
            30
        )

        self.draw_asteroid(
            screen,
            self.screen_width - 60,
            315,
            22
        )

        self.draw_side_ship(
            screen,
            50,
            355,
            0.65,
            1
        )

        self.draw_side_ship(
            screen,
            self.screen_width - 50,
            220,
            0.65,
            -1
        )

        self.draw_planet(screen)
        self.draw_wireframe_floor(screen)

        border = pygame.Rect(
            12,
            12,
            self.screen_width - 24,
            self.screen_height - 24
        )

        self.draw_neon_rect(
            screen,
            border,
            self.pink,
            2
        )

    def draw_input(
        self,
        screen,
        rect,
        label,
        value,
        active=False,
        password=False,
        visible=False,
        eye_rect=None
    ):
        label_surface = self.label_font.render(
            label,
            True,
            self.light_pink
        )

        screen.blit(
            label_surface,
            (rect.x, rect.y - 21)
        )

        self.draw_neon_rect(
            screen,
            rect,
            self.bright_pink if active else self.pink,
            2
        )

        display_value = value

        if password and not visible:
            display_value = "•" * len(value)

        text_surface = self.input_font.render(
            display_value,
            True,
            self.white
        )

        screen.blit(
            text_surface,
            (
                rect.x + 12,
                rect.y + 11
            )
        )

        if active and self.cursor_timer < 30:
            cursor_x = (
                rect.x +
                12 +
                text_surface.get_width() +
                2
            )

            max_x = (
                rect.right - 42
                if password
                else rect.right - 10
            )

            cursor_x = min(
                cursor_x,
                max_x
            )

            pygame.draw.line(
                screen,
                self.bright_pink,
                (cursor_x, rect.y + 9),
                (cursor_x, rect.bottom - 9),
                2
            )

        if password and eye_rect:
            eye_color = (
                self.bright_pink
                if visible
                else self.gray
            )

            pygame.draw.ellipse(
                screen,
                eye_color,
                (
                    eye_rect.x + 2,
                    eye_rect.y + 6,
                    eye_rect.width - 4,
                    eye_rect.height - 12
                ),
                2
            )

            pygame.draw.circle(
                screen,
                eye_color,
                eye_rect.center,
                3
            )

            if not visible:
                pygame.draw.line(
                    screen,
                    eye_color,
                    (
                        eye_rect.left + 2,
                        eye_rect.bottom - 3
                    ),
                    (
                        eye_rect.right - 2,
                        eye_rect.top + 3
                    ),
                    2
                )

    def draw_button(self, screen, rect, text, ship=True):
        hover = rect.collidepoint(
            pygame.mouse.get_pos()
        )

        color = (
            self.bright_pink
            if hover
            else self.pink
        )

        pygame.draw.rect(
            screen,
            (55, 6, 48),
            rect,
            border_radius=4
        )

        self.draw_neon_rect(
            screen,
            rect,
            color,
            2
        )

        if ship:
            self.draw_spaceship(
                screen,
                rect.x + 30,
                rect.centery,
                0.28
            )

        text_surface = self.button_font.render(
            text,
            True,
            self.white
        )

        offset = 10 if ship else 0

        screen.blit(
            text_surface,
            (
                rect.centerx -
                text_surface.get_width() // 2 +
                offset,
                rect.centery -
                text_surface.get_height() // 2
            )
        )

    def draw_menu(self, screen):
        self.draw_background(screen)
        self.draw_hud(screen)

        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            100,
            0.60
        )

        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                cx -
                title.get_width() // 2,
                145
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 220, 205),
            (cx + 220, 205),
            1
        )

        self.draw_button(
            screen,
            self.login_btn_rect,
            "LOG IN"
        )

        self.draw_button(
            screen,
            self.signup_btn_rect,
            "SIGN UP"
        )

        self.draw_help(screen)

    def draw_auth_form(self, screen, mode):
        self.draw_background(screen)
        self.draw_hud(screen)

        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            92,
            0.55
        )

        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                cx -
                title.get_width() // 2,
                125
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 230, 190),
            (cx + 230, 190),
            1
        )

        section = (
            "LOG IN"
            if mode == "login"
            else "SIGN UP"
        )

        section_surface = self.section_font.render(
            section,
            True,
            self.light_pink
        )

        screen.blit(
            section_surface,
            (
                cx -
                section_surface.get_width() // 2,
                200
            )
        )

        self.draw_input(
            screen,
            self.username_rect,
            "USERNAME",
            self.username,
            self.active_field == "username"
        )

        self.draw_input(
            screen,
            self.password_rect,
            "PASSWORD",
            self.password,
            self.active_field == "password",
            True,
            self.show_password,
            self.pass_eye_rect
        )

        if mode == "login":
            hover = self.forgot_pass_rect.collidepoint(
                pygame.mouse.get_pos()
            )

            forgot_surface = self.small_font.render(
                "FORGOT PASSWORD?",
                True,
                self.bright_pink
                if hover
                else self.light_pink
            )

            screen.blit(
                forgot_surface,
                (
                    self.forgot_pass_rect.right -
                    forgot_surface.get_width(),
                    self.forgot_pass_rect.y
                )
            )

        else:
            self.draw_input(
                screen,
                self.confirm_rect,
                "CONFIRM PASSWORD",
                self.confirm_password,
                self.active_field == "confirm",
                True,
                self.show_confirm,
                self.confirm_eye_rect
            )

        self.draw_button(
            screen,
            self.back_btn_rect,
            "BACK",
            False
        )

        self.draw_button(
            screen,
            self.submit_btn_rect,
            "LOG IN" if mode == "login" else "CREATE"
        )

        if self.error_msg:
            error_y = 515

            error_surface = self.error_font.render(
                self.error_msg,
                True,
                self.error_color
            )

            screen.blit(
                error_surface,
                (
                    cx -
                    error_surface.get_width() // 2,
                    error_y
                )
            )

        self.draw_help(screen)

    def draw_help(self, screen):
        cx = self.screen_width // 2

        pygame.draw.line(
            screen,
            self.deep_pink,
            (
                cx - 180,
                self.screen_height - 52
            ),
            (
                cx + 180,
                self.screen_height - 52
            ),
            1
        )

        hover = self.help_center_rect.collidepoint(
            pygame.mouse.get_pos()
        )

        text = self.small_font.render(
            "HELP CENTER",
            True,
            self.bright_pink if hover else self.white
        )

        screen.blit(
            text,
            (
                cx -
                text.get_width() // 2,
                self.screen_height - 28
            )
        )

    def draw(self, screen, mode=None):
        if mode is not None:
            self.mode = mode

        self.update()

        if self.mode == "menu":
            self.draw_menu(screen)
        else:
            self.draw_auth_form(
                screen,
                self.mode
            )

    def handle_event(self, event, mode=None):
        if mode is not None:
            self.mode = mode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            if self.mode == "menu":

                if self.login_btn_rect.collidepoint(pos):
                    self.set_mode("login")
                    return None

                if self.signup_btn_rect.collidepoint(pos):
                    self.set_mode("signup")
                    return None

                if self.help_center_rect.collidepoint(pos):
                    return "help_center"

                return None

            if self.pass_eye_rect.collidepoint(pos):
                self.show_password = not self.show_password
                self.active_field = "password"
                self.cursor_timer = 0
                return None

            if (
                self.mode == "signup"
                and self.confirm_eye_rect.collidepoint(pos)
            ):
                self.show_confirm = not self.show_confirm
                self.active_field = "confirm"
                self.cursor_timer = 0
                return None

            if (
                self.mode == "login"
                and self.forgot_pass_rect.collidepoint(pos)
            ):
                return "forgot_password"

            if self.help_center_rect.collidepoint(pos):
                return "help_center"

            if self.username_rect.collidepoint(pos):
                self.active_field = "username"
                self.cursor_timer = 0
                return None

            if self.password_rect.collidepoint(pos):
                self.active_field = "password"
                self.cursor_timer = 0
                return None

            if (
                self.mode == "signup"
                and self.confirm_rect.collidepoint(pos)
            ):
                self.active_field = "confirm"
                self.cursor_timer = 0
                return None

            if self.submit_btn_rect.collidepoint(pos):
                return "submit"

            if self.back_btn_rect.collidepoint(pos):
                self.set_mode("menu")
                return "back"

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                if self.mode != "menu":
                    self.set_mode("menu")
                    return "back"

                return "quit"

            if self.mode == "menu":
                return None

            if event.key == pygame.K_RETURN:
                return "submit"

            if event.key == pygame.K_TAB:

                if self.mode == "login":

                    if self.active_field == "username":
                        self.active_field = "password"
                    else:
                        self.active_field = "username"

                else:

                    if self.active_field == "username":
                        self.active_field = "password"

                    elif self.active_field == "password":
                        self.active_field = "confirm"

                    else:
                        self.active_field = "username"

                self.cursor_timer = 0

            elif event.key == pygame.K_BACKSPACE:

                if self.active_field == "username":
                    self.username = self.username[:-1]

                elif self.active_field == "password":
                    self.password = self.password[:-1]

                elif self.active_field == "confirm":
                    self.confirm_password = self.confirm_password[:-1]

                self.cursor_timer = 0

            elif event.unicode and event.unicode.isprintable():

                if (
                    self.active_field == "username"
                    and len(self.username) < 18
                ):
                    self.username += event.unicode

                elif (
                    self.active_field == "password"
                    and len(self.password) < 18
                ):
                    self.password += event.unicode

                elif (
                    self.active_field == "confirm"
                    and len(self.confirm_password) < 18
                ):
                    self.confirm_password += event.unicode

                self.cursor_timer = 0

        return None