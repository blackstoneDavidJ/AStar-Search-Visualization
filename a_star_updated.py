import pygame, sys
import pygame_gui
import algo_methods
import random
from algo_methods import GRID_DIM, gridSquare, SQUARE_SIZE, gridSquareEdges

def main_app() -> None:
    """Function to run the main GUI display. Contains a window manager and all elements
    """

    ## Main Menu Elements 
    gridS = gridSquare
    gridSE = gridSquareEdges

    maze_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((200, 180), (200, 50)),
                                            text='MAZE',
                                            manager=manager)

    settings_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((200, 250), (200, 50)),
                                            text='SETTINGS',
                                            manager=manager)

    exit_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((200, 320), (200, 50)),
                                            text='EXIT',
                                            manager=manager)
    
    escape_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((100, 420), (400,50)),
        text="Press the ESC key to go back at any time",
        manager=manager
    )

    main_menu_element_list = [maze_button, 
                             settings_button, 
                             exit_button,
                             escape_label]

    ## Maze Screen Elements 

    new_maze_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((25, 20), (150, 50)),
                                            text='NEW MAZE',
                                            manager=manager)
    
    solve_maze_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((225, 20), (150, 50)),
                                            text='SOLVE',
                                            manager=manager)
    
    reset_maze_button = pygame_gui.elements.UIButton(
                                            relative_rect=pygame.Rect((425, 20), (150, 50)),
                                            text='RESET',
                                            manager=manager)
    
    maze_screen_elements_list = [new_maze_button, 
                                solve_maze_button,
                                reset_maze_button]

    ## Settings Screen Buttons

    settings_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((100, 300), (400,50)),
        text="Nothing to see here yet",
        manager=manager
    )

    settings_screen_elements_list = [settings_label]

    ## Method to display buttons
    def show_buttons(names:list) -> None:
        """Nested function to show the buttons after passing in a list of names
        Args:
        names (list): list of button names 
        """

        for i in names: i.show()

    ## Method to hide buttons
    def hide_buttons(names:list) -> None:
        """Nested function to hide the buttons after passing in a list of names
        Args:
        names (list): list of button names 
        """

        for i in names: i.hide()

    def get_square(x, y) -> pygame.Rect:
        return pygame.Rect(
                        SQUARE_SIZE * x + 50, 
                        SQUARE_SIZE * y + 80, 
                        SQUARE_SIZE, 
                        SQUARE_SIZE)
    def get_circle(x, y) -> list:
        center_x = SQUARE_SIZE * x + 50 + SQUARE_SIZE // 2
        center_y = SQUARE_SIZE * y + 80 + SQUARE_SIZE // 2
        
        # Specify the radius of the circle
        radius = 40 // 2
        return [center_x, center_y, radius]
    ## Method to draw the maze grid 
    def draw_grid() -> None:
        for x in range(GRID_DIM):
            for y in range(GRID_DIM):

                rect = get_square(x, y)
                circle_pieces = get_circle(x, y)
                if gridS[x][y] == 1:
                    color = (255,255,255)
                elif gridS[x][y] == 2:
                    color = (0,255,0)
                elif gridS[x][y] == 3:
                    color = (255,0,0)
                elif gridS[x][y] == 5:
                    color = (255, 0, 255)
                else:
                    color = (0,0,0)
                if gridS[x][y] in [1, 5] or color == (0,0,0): 
                    pygame.draw.rect(background, color, rect)
                else:
                    pygame.draw.circle(background, color, (circle_pieces[0], circle_pieces[1]), circle_pieces[2])

                wallWidth = 2
                wallColor = (255, 255, 255)
                for edge in gridSE[x][y].faces:
                    if edge is "NORTH":
                        pygame.draw.line(background, wallColor, rect.topleft, rect.topright, wallWidth)
                    if edge is "SOUTH":
                        pygame.draw.line(background, wallColor, rect.bottomleft, rect.bottomright, wallWidth)
                    if edge is "EAST":
                        pygame.draw.line(background, wallColor, rect.topright, rect.bottomright, wallWidth)
                    if edge is "WEST":
                        pygame.draw.line(background, wallColor, rect.topleft, rect.bottomleft, wallWidth)

    ## Invoking methods to hide button elements on startup
    hide_buttons(maze_screen_elements_list)
    hide_buttons(settings_screen_elements_list)

    ## MAIN EVENT LOOP

    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                
                # Main Menu button handlers

                if event.ui_element == maze_button:
                    background.blit(background_image, (0,0))
                    hide_buttons(main_menu_element_list)
                    show_buttons(maze_screen_elements_list)
                    draw_grid()
                
                if event.ui_element == settings_button:
                    background.blit(background_image, (0,0))
                    hide_buttons(main_menu_element_list)
                    show_buttons(settings_screen_elements_list)
                    
                if event.ui_element == exit_button:
                    pygame.quit()
                    sys.exit()

                # Maze Screen button handlers

                if event.ui_element == new_maze_button:
                    algo_methods.startPlaced = False
                    grids = algo_methods.create_random_maze()

                    gridS = grids[0]
                    gridSE = grids[1]

                    algo_methods.queueList.clear()
                    algo_methods.nodeList.clear()
                    algo_methods.distanceArray.clear()
                    algo_methods.init_arrays()
                    gridS[0][0] = 2
                    gridS[algo_methods.endX][algo_methods.endY] = 3
                    draw_grid()
                
                if event.ui_element == solve_maze_button:
                    algo_methods.solve_a_star_maze()
                    gridS[algo_methods.endX][algo_methods.endY] = 3
                    draw_grid()

                if event.ui_element == reset_maze_button:
                    algo_methods.startPlaced = False
                    algo_methods.clear_grid()
                    algo_methods.queueList.clear()
                    algo_methods.nodeList.clear()
                    algo_methods.distanceArray.clear()
                    algo_methods.init_arrays()
                    gridS[0][0] = 2
                    gridS[algo_methods.endX][algo_methods.endY] = 3
                    draw_grid()
            
            # General App handlers
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    hide_buttons(maze_screen_elements_list)
                    hide_buttons(settings_screen_elements_list)
                    background.blit(background_image, (0,0))
                    background.blit(title_image, (105, 50))
                    show_buttons(main_menu_element_list)        

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.set_caption(f"A* Search Algorithm ~~ ")
        pygame.display.flip()


if __name__ == "__main__":

    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption(f"A* Search Algorithm ~~")
    window_surface = pygame.display.set_mode((600, 600))

    background_image = pygame.image.load("reqs/800gradient.jpg")
    title_image = pygame.image.load("reqs/title.png")

    background = pygame.Surface((600, 600))
    background.fill(pygame.Color('#000000'))
    background.blit(background_image, (0,0))
    background.blit(title_image, (105, 50))

    manager = pygame_gui.UIManager((600, 600))
    manager.get_theme().load_theme("reqs/base_theme.json")

    main_app()