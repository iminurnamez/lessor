from . import prepare,tools
from .states import title_screen, gameplay, show_window, splash_screen, win_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "GAMEPLAY": gameplay.Gameplay(),
                   "SHOW_WINDOW": show_window.ShowWindow(), 
                   "SPLASH": splash_screen.SplashScreen(),
                   "WIN_SCREEN": win_screen.WinScreen()}
    controller.setup_states(states, "SPLASH")
    controller.main()
