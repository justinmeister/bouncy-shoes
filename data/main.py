from data.states import main_menu
from data.states import level
from . import setup, tools

MAIN_MENU = 'main menu'
LEVEL1 = 'level1'

def main():
    """
    Add states to control here.
    """
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu(),
                  LEVEL1: level.Level(LEVEL1)
                  }

    run_it.setup_states(state_dict, MAIN_MENU)
    run_it.main()

