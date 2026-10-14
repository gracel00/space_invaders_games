import pygame

from managers.auth import AuthUI
from managers.game_manager import GameManager
from managers.home import HomeUI
from managers.leaderboard import LeaderboardUI
from managers.user_profile import UserProfileUI
from managers.settings_manager import SettingsUI


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "Space Invaders by Dinglasa, Gracel T."
)

auth = AuthUI(
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

home = None

leaderboard = LeaderboardUI(
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

user_profile = UserProfileUI(
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

settings = SettingsUI(
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

game = GameManager(
    screen,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

current_screen = "auth"
previous_screen = "home"

clock = pygame.time.Clock()
running = True


while running:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            running = False
            continue

        if current_screen == "auth":

            action = auth.handle_event(event)

            if action == "submit":

                if auth.submit(auth.mode):

                    home = HomeUI(
                        SCREEN_WIDTH,
                        SCREEN_HEIGHT
                    )

                    current_screen = "home"

            elif action == "back":

                current_screen = "auth"

            elif action == "quit":

                running = False

        elif current_screen == "home":

            action = home.handle_event(event)

            if action == "start_game":

                if auth.current_user:

                    game.current_player_id = (
                        auth.current_user["player_id"]
                    )

                    game.player_name = (
                        auth.current_user["username"]
                    )

                    game.mobile_controls_enabled = (
                        settings.controls_on
                    )

                    game.reset_game_vars()
                    game.game_state = "playing"

                    current_screen = "game"

            elif action == "leaderboard":

                leaderboard.load_data()
                leaderboard.reset_scroll()

                current_screen = "leaderboard"

            elif action == "profile":

                if auth.current_user:

                    user_profile.set_user(
                        auth.current_user["player_id"],
                        auth.current_user["username"]
                    )

                    current_screen = "profile"

            elif action == "settings":

                previous_screen = "home"
                current_screen = "settings"

            elif action == "logout":

                auth.current_user = None
                auth.set_mode("menu")

                home = None
                current_screen = "auth"

        elif current_screen == "profile":

            action = user_profile.handle_event(event)

            if action == "back":

                home = HomeUI(
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )

                current_screen = "home"

            elif action == "deleted":

                auth.current_user = None
                auth.set_mode("menu")

                home = None
                current_screen = "auth"

        elif current_screen == "leaderboard":

            action = leaderboard.handle_event(event)

            if action == "back":

                home = HomeUI(
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                )

                current_screen = "home"

        elif current_screen == "settings":

            action = settings.handle_event(event)

            if action == "controls_toggle":

                game.mobile_controls_enabled = (
                    settings.controls_on
                )

            elif action == "back":

                game.mobile_controls_enabled = (
                    settings.controls_on
                )

                current_screen = previous_screen

        elif current_screen == "game":

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):

                previous_screen = "game"
                current_screen = "settings"

    if current_screen == "auth":

        auth.draw(screen)

    elif current_screen == "home":

        username = ""

        if auth.current_user:
            username = auth.current_user["username"]

        home.draw(
            screen,
            username
        )

    elif current_screen == "profile":

        user_profile.draw(screen)

    elif current_screen == "leaderboard":

        leaderboard.draw(screen)

    elif current_screen == "settings":

        settings.draw(screen)

    elif current_screen == "game":

        result = game.update(events)

        if result == "back_home":

            game.game_state = "playing"

            home = HomeUI(
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )

            current_screen = "home"

    pygame.display.flip()

    clock.tick(60)


pygame.quit()