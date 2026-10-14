import pygame
import random
import math
import mysql.connector
from mysql.connector import Error


class UserProfileUI:

    def __init__(self, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        # ==================================================
        # FONTS
        # ==================================================

        self.title_font = pygame.font.SysFont(
            "consolas", 42, bold=True
        )

        self.button_font = pygame.font.SysFont(
            "consolas", 18, bold=True
        )

        self.small_font = pygame.font.SysFont(
            "consolas", 12, bold=True
        )

        self.input_font = pygame.font.SysFont(
            "consolas", 20, bold=True
        )

        # ==================================================
        # COLORS
        # ==================================================

        self.bg = (7, 2, 14)
        self.pink = (255, 45, 180)
        self.light_pink = (255, 130, 225)
        self.bright_pink = (255, 215, 250)

        self.white = (255, 245, 255)
        self.gray = (180, 155, 180)

        self.grid_color = (75, 12, 70)
        self.deep_pink = (100, 15, 90)

        # ==================================================
        # PROFILE BOXES
        # ==================================================

        cx = screen_width // 2

        profile_width = 380
        profile_height = 55

        self.username_rect = pygame.Rect(
            cx - profile_width // 2,
            int(screen_height * 0.40),
            profile_width,
            profile_height
        )

        self.best_score_rect = pygame.Rect(
            cx - profile_width // 2,
            int(screen_height * 0.50),
            profile_width,
            profile_height
        )

        self.current_score_rect = pygame.Rect(
            cx - profile_width // 2,
            int(screen_height * 0.60),
            profile_width,
            profile_height
        )

        # ==================================================
        # BUTTONS
        # ==================================================

        # EDIT PROFILE - LEFT
        self.edit_rect = pygame.Rect(
            35,
            screen_height - 65,
            190,
            40
        )

        # BACK - RIGHT
        self.back_rect = pygame.Rect(
            screen_width - 180,
            screen_height - 65,
            150,
            40
        )

        # ==================================================
        # EDIT PROFILE PANEL
        # ==================================================

        self.edit_panel = pygame.Rect(
            150,
            155,
            500,
            290
        )

        self.username_input = pygame.Rect(
            200,
            230,
            400,
            48
        )

        self.save_rect = pygame.Rect(
            200,
            310,
            120,
            42
        )

        self.cancel_rect = pygame.Rect(
            340,
            310,
            120,
            42
        )

        self.delete_rect = pygame.Rect(
            480,
            310,
            120,
            42
        )

        # ==================================================
        # USER DATA
        # ==================================================

        self.player_id = None
        self.username = "Player"

        self.best_score = 0
        self.current_score = 0

        # ==================================================
        # EDIT STATE
        # ==================================================

        self.editing = False
        self.edit_username = ""
        self.input_active = False
        self.message = ""

        # ==================================================
        # STARS
        # ==================================================

        random.seed(10)

        self.stars = [
            (
                random.randint(20, screen_width - 20),
                random.randint(55, screen_height - 100),
                random.choice([1, 1, 1, 2])
            )
            for _ in range(65)
        ]

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    def get_connection(self):

        try:

            connection = mysql.connector.connect(
                host="localhost",
                port=3306,
                database="space_invaders_db",
                user="root",
                password=""
            )

            if connection.is_connected():
                return connection

        except Error:
            return None

        return None

    # ==================================================
    # SET USER
    # ==================================================

    def set_user(
        self,
        player_id,
        username,
        current_score=None
    ):

        self.player_id = player_id
        self.username = username or "Player"

        self.editing = False
        self.input_active = False
        self.message = ""

        self.load_user_data()

        if current_score is not None:
            self.current_score = int(current_score)

    # ==================================================
    # READ
    # ==================================================

    def load_user_data(self):

        if self.player_id is None:
            return

        connection = None
        cursor = None

        try:

            connection = self.get_connection()

            if connection is None:
                return

            cursor = connection.cursor()

            # USERNAME
            cursor.execute(
                """
                SELECT username
                FROM players
                WHERE player_id = %s
                LIMIT 1
                """,
                (self.player_id,)
            )

            result = cursor.fetchone()

            if result:
                self.username = result[0] or "Player"

            # HIGHEST SCORE
            cursor.execute(
                """
                SELECT COALESCE(MAX(score), 0)
                FROM scores
                WHERE player_id = %s
                """,
                (self.player_id,)
            )

            result = cursor.fetchone()

            self.best_score = int(
                result[0] or 0
            )

            # CURRENT / LATEST SCORE
            cursor.execute(
                """
                SELECT score
                FROM scores
                WHERE player_id = %s
                ORDER BY score_id DESC
                LIMIT 1
                """,
                (self.player_id,)
            )

            result = cursor.fetchone()

            if result:
                self.current_score = int(
                    result[0] or 0
                )
            else:
                self.current_score = 0

        except Error:

            self.best_score = 0
            self.current_score = 0

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ==================================================
    # CREATE
    # ==================================================

    def create_score(self, score):

        if self.player_id is None:
            return False

        connection = None
        cursor = None

        try:

            connection = self.get_connection()

            if connection is None:
                return False

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO scores
                (player_id, score)
                VALUES (%s, %s)
                """,
                (
                    self.player_id,
                    int(score)
                )
            )

            connection.commit()

            self.load_user_data()

            return True

        except Error:

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ==================================================
    # UPDATE USERNAME
    # ==================================================

    def update_username(self, new_username):

        if self.player_id is None:
            return False

        new_username = new_username.strip()

        if not new_username:
            self.message = "USERNAME CANNOT BE EMPTY"
            return False

        if len(new_username) > 20:
            self.message = "USERNAME TOO LONG"
            return False

        connection = None
        cursor = None

        try:

            connection = self.get_connection()

            if connection is None:
                self.message = "DATABASE ERROR"
                return False

            cursor = connection.cursor()

            # CHECK DUPLICATE USERNAME
            cursor.execute(
                """
                SELECT player_id
                FROM players
                WHERE username = %s
                AND player_id != %s
                LIMIT 1
                """,
                (
                    new_username,
                    self.player_id
                )
            )

            if cursor.fetchone():

                self.message = "USERNAME ALREADY EXISTS"
                return False

            # UPDATE
            cursor.execute(
                """
                UPDATE players
                SET username = %s
                WHERE player_id = %s
                """,
                (
                    new_username,
                    self.player_id
                )
            )

            connection.commit()

            self.username = new_username
            self.message = "PROFILE UPDATED"

            return True

        except Error:

            if connection:
                connection.rollback()

            self.message = "UPDATE FAILED"

            return False

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ==================================================
    # DELETE USER
    # ==================================================

    def delete_user(self):

        if self.player_id is None:
            return False

        connection = None
        cursor = None

        try:

            connection = self.get_connection()

            if connection is None:
                return False

            cursor = connection.cursor()

            # DELETE SCORES FIRST
            cursor.execute(
                """
                DELETE FROM scores
                WHERE player_id = %s
                """,
                (self.player_id,)
            )

            # DELETE ACCOUNT
            cursor.execute(
                """
                DELETE FROM players
                WHERE player_id = %s
                """,
                (self.player_id,)
            )

            connection.commit()

            self.player_id = None
            self.username = "Player"
            self.best_score = 0
            self.current_score = 0

            return True

        except Error:

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ==================================================
    # NEON RECT
    # ==================================================

    def draw_neon_rect(
        self,
        screen,
        rect,
        color,
        width=2
    ):

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

    # ==================================================
    # STARS
    # ==================================================

    def draw_stars(self, screen):

        for x, y, size in self.stars:

            pygame.draw.circle(
                screen,
                self.light_pink,
                (x, y),
                size
            )

    # ==================================================
    # SPACESHIP
    # ==================================================

    def draw_spaceship(
        self,
        screen,
        x,
        y,
        scale=1.0
    ):

        points = [
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
            points
        )

        pygame.draw.lines(
            screen,
            self.light_pink,
            True,
            points,
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

    # ==================================================
    # SIDE SHIP
    # ==================================================

    def draw_side_ship(
        self,
        screen,
        x,
        y,
        scale=1.0,
        direction=1
    ):

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

    # ==================================================
    # PLANET
    # ==================================================

    def draw_planet(self, screen):

        cx = self.screen_width // 2
        cy = self.screen_height + 80
        radius = 150

        for r in range(radius, 0, -5):

            ratio = r / radius

            color = (
                int(55 * ratio),
                int(6 * ratio),
                int(48 * ratio)
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

    # ==================================================
    # GRID
    # ==================================================

    def draw_grid(self, screen):

        horizon = int(
            self.screen_height * 0.74
        )

        for row in range(12):

            y = horizon + row * 18

            pygame.draw.line(
                screen,
                self.grid_color,
                (0, y),
                (self.screen_width, y),
                1
            )

        center = self.screen_width // 2

        for x in range(
            -self.screen_width,
            self.screen_width * 2,
            40
        ):

            top_x = center + (
                x - center
            ) * 0.15

            pygame.draw.line(
                screen,
                self.grid_color,
                (int(top_x), horizon),
                (x, self.screen_height),
                1
            )

    # ==================================================
    # HUD
    # ==================================================

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

    # ==================================================
    # BACKGROUND
    # ==================================================

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
        self.draw_grid(screen)
        self.draw_planet(screen)

        self.draw_side_ship(
            screen,
            50,
            270,
            0.65,
            1
        )

        self.draw_side_ship(
            screen,
            self.screen_width - 50,
            310,
            0.65,
            -1
        )

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

    # ==================================================
    # PROFILE INFO
    # ==================================================

    def draw_profile_info(
        self,
        screen,
        rect,
        label,
        value
    ):

        pygame.draw.rect(
            screen,
            (50, 6, 45),
            rect,
            border_radius=5
        )

        self.draw_neon_rect(
            screen,
            rect,
            self.pink,
            2
        )

        label_surface = self.button_font.render(
            label,
            True,
            self.white
        )

        screen.blit(
            label_surface,
            (
                rect.left + 25,
                rect.centery -
                label_surface.get_height() // 2
            )
        )

        value_surface = self.button_font.render(
            str(value),
            True,
            self.light_pink
        )

        screen.blit(
            value_surface,
            (
                rect.right -
                value_surface.get_width() -
                25,
                rect.centery -
                value_surface.get_height() // 2
            )
        )

    # ==================================================
    # BUTTON
    # ==================================================

    def draw_button(
        self,
        screen,
        rect,
        text
    ):

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
            (50, 6, 45),
            rect,
            border_radius=5
        )

        self.draw_neon_rect(
            screen,
            rect,
            color,
            2
        )

        text_surface = self.button_font.render(
            text,
            True,
            self.white
        )

        screen.blit(
            text_surface,
            (
                rect.centerx -
                text_surface.get_width() // 2,
                rect.centery -
                text_surface.get_height() // 2
            )
        )

    # ==================================================
    # EDIT PROFILE PANEL
    # ==================================================

    def draw_edit_panel(self, screen):

        # DARK OVERLAY
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))

        screen.blit(
            overlay,
            (0, 0)
        )

        # PANEL
        pygame.draw.rect(
            screen,
            (25, 3, 25),
            self.edit_panel,
            border_radius=8
        )

        self.draw_neon_rect(
            screen,
            self.edit_panel,
            self.pink,
            2
        )

        title = self.button_font.render(
            "EDIT PROFILE",
            True,
            self.bright_pink
        )

        screen.blit(
            title,
            (
                self.edit_panel.centerx -
                title.get_width() // 2,
                180
            )
        )

        label = self.small_font.render(
            "USERNAME",
            True,
            self.white
        )

        screen.blit(
            label,
            (200, 210)
        )

        # INPUT
        input_color = (
            self.bright_pink
            if self.input_active
            else self.pink
        )

        pygame.draw.rect(
            screen,
            (50, 6, 45),
            self.username_input,
            border_radius=5
        )

        self.draw_neon_rect(
            screen,
            self.username_input,
            input_color,
            2
        )

        text = self.input_font.render(
            self.edit_username,
            True,
            self.white
        )

        screen.blit(
            text,
            (
                self.username_input.left + 12,
                self.username_input.centery -
                text.get_height() // 2
            )
        )

        # BUTTONS
        self.draw_button(
            screen,
            self.save_rect,
            "SAVE"
        )

        self.draw_button(
            screen,
            self.cancel_rect,
            "CANCEL"
        )

        self.draw_button(
            screen,
            self.delete_rect,
            "DELETE"
        )

        # MESSAGE
        if self.message:

            message = self.small_font.render(
                self.message,
                True,
                self.light_pink
            )

            screen.blit(
                message,
                (
                    self.edit_panel.centerx -
                    message.get_width() // 2,
                    370
                )
            )

    # ==================================================
    # DRAW
    # ==================================================

    def draw(self, screen):

        # Refresh scores/data
        self.load_user_data()

        self.draw_background(screen)
        self.draw_hud(screen)

        cx = self.screen_width // 2

        self.draw_spaceship(
            screen,
            cx,
            92,
            0.65
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
                130
            )
        )

        pygame.draw.line(
            screen,
            self.deep_pink,
            (cx - 220, 180),
            (cx + 220, 180),
            1
        )

        welcome = self.small_font.render(
            f"WELCOME! {self.username}",
            True,
            self.light_pink
        )

        screen.blit(
            welcome,
            (
                cx -
                welcome.get_width() // 2,
                195
            )
        )

        # USERNAME
        self.draw_profile_info(
            screen,
            self.username_rect,
            "USERNAME",
            self.username
        )

        # HIGHEST SCORE
        self.draw_profile_info(
            screen,
            self.best_score_rect,
            "HIGHEST SCORE",
            self.best_score
        )

        # CURRENT SCORE
        self.draw_profile_info(
            screen,
            self.current_score_rect,
            "CURRENT SCORE",
            self.current_score
        )

        # EDIT PROFILE
        self.draw_button(
            screen,
            self.edit_rect,
            "EDIT PROFILE"
        )

        # BACK
        self.draw_button(
            screen,
            self.back_rect,
            "BACK"
        )

        # EDIT PANEL
        if self.editing:
            self.draw_edit_panel(screen)

    # ==================================================
    # EVENTS
    # ==================================================

    def handle_event(self, event):

        # ==================================================
        # EDIT MODE
        # ==================================================

        if self.editing:

            # TEXT INPUT
            if event.type == pygame.TEXTINPUT:

                if self.input_active:

                    if len(self.edit_username) < 20:

                        self.edit_username += event.text

                return None

            # KEYBOARD
            if event.type == pygame.KEYDOWN:

                if self.input_active:

                    if event.key == pygame.K_BACKSPACE:

                        self.edit_username = (
                            self.edit_username[:-1]
                        )

                    elif event.key == pygame.K_RETURN:

                        self.save_profile()

                    elif event.key == pygame.K_ESCAPE:

                        self.editing = False
                        self.input_active = False
                        self.message = ""

                return None

            # MOUSE
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                # INPUT
                if self.username_input.collidepoint(
                    event.pos
                ):

                    self.input_active = True
                    return None

                # SAVE
                if self.save_rect.collidepoint(
                    event.pos
                ):

                    self.save_profile()
                    return None

                # CANCEL
                if self.cancel_rect.collidepoint(
                    event.pos
                ):

                    self.editing = False
                    self.input_active = False
                    self.message = ""

                    return None

                # DELETE
                if self.delete_rect.collidepoint(
                    event.pos
                ):

                    if self.delete_user():

                        self.editing = False
                        self.input_active = False

                        return "deleted"

                    self.message = "DELETE FAILED"

                return None

            return None

        # ==================================================
        # NORMAL PROFILE
        # ==================================================

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            # EDIT PROFILE
            if self.edit_rect.collidepoint(
                event.pos
            ):

                self.editing = True
                self.input_active = True
                self.edit_username = self.username
                self.message = ""

                pygame.key.start_text_input()

                return None

            # BACK
            if self.back_rect.collidepoint(
                event.pos
            ):

                pygame.key.stop_text_input()

                return "back"

        return None

    # ==================================================
    # SAVE PROFILE
    # ==================================================

    def save_profile(self):

        new_username = self.edit_username.strip()

        if not new_username:

            self.message = "USERNAME CANNOT BE EMPTY"
            return

        if self.update_username(new_username):

            self.editing = False
            self.input_active = False

            pygame.key.stop_text_input()

            self.message = ""

        else:

            # Keep edit panel open if update fails
            self.input_active = True