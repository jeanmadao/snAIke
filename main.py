#Made with lots of clumsiness and love by Jean Pierre HUYNH.
import pygame, random, time

TITLE = "snAIke!"
FPS = 30
BLACK = (50, 50, 50)
GREY = (120, 120, 120)
WHITE = (200, 200, 200)
YELLOW = (200, 200, 50)
RED = (200, 50, 50)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)
SNAKE_CHAR = '+'
EMPTY_CHAR = ' '
WALL_CHAR = '#'
FOOD_CHAR = '@'

class Game:
    def __init__(self):
        self.run = True
        self.rows = 20
        self.columns = 20
        self.grid = [[' ' for j in range(100)] for i in range(100)]
        self.snake = []
        self.previous_move = None
        self.next_move = None
        self.food = None
        self.alive = False
        self.score = 0
        self.best_score = 0
        self.start_time = time.time()
        self.current_time = self.start_time
        self.mps = 15

    def is_running(self):
        return self.run

    def stop_running(self):
        self.run = False

    def speedup(self):
        if self.mps < 50:
            self.mps += 1
        self.score = 0
        self.best_score = 0

    def slowdown(self):
        if self.mps > 1:
            self.mps -=1
        self.score = 0
        self.best_score = 0

    def get_mps(self):
        return self.mps

    def reset_grid(self):
        for i in range(100):
            for j in range(100):
                self.grid[i][j] = EMPTY_CHAR
        self.score = 0
        self.best_score = 0

    def expand_row(self):
        if self.rows < 100:
            self.rows += 1
        self.score = 0
        self.best_score = 0

    def expand_column(self):
        if self.columns < 100:
            self.columns += 1
        self.score = 0
        self.best_score = 0

    def shrink_row(self):
        if self.rows > 1:
            self.rows -= 1
        self.score = 0
        self.best_score = 0

    def shrink_column(self):
        if self.columns > 1:
            self.columns -= 1
        self.score = 0
        self.best_score = 0

    def is_alive(self):
        return self.alive

    def remove_food(self):
        if self.food is not None and self.grid[self.food[0]][self.food[1]] == FOOD_CHAR:
            self.grid[self.food[0]][self.food[1]] = EMPTY_CHAR
        self.food = None

    def remove_snake(self):
        for i in range(len(self.snake)):
            pos = self.snake.pop()
            if self.grid[pos[0]][pos[1]] == SNAKE_CHAR:
                self.grid[pos[0]][pos[1]] = EMPTY_CHAR

    def get_available_cells(self):
        available_cells = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] == EMPTY_CHAR:
                    available_cells.append((i, j))
        return available_cells

    def get_random_cell(self):
        random_cell = None
        available_cells = self.get_available_cells()
        if len(available_cells) > 0:
            random_cell = random.choice(available_cells)
        return random_cell

    def spawn_snake(self):
        random_cell = self.get_random_cell()
        if random_cell is None:
            self.alive = False
        else:
            self.snake.insert(0, random_cell)
            self.grid[random_cell[0]][random_cell[1]] = SNAKE_CHAR

    def spawn_food(self):
        random_cell = self.get_random_cell()
        if random_cell is None:
            self.alive = False
        else:
            self.grid[random_cell[0]][random_cell[1]] = FOOD_CHAR
            self.food = random_cell

    def start_run(self):
        self.remove_food()
        self.remove_snake()
        self.alive = True
        self.score = 0
        self.previous_move = None
        self.next_move = None
        self.spawn_snake()
        self.spawn_food()
        self.start_time = time.time()
        self.current_time = self.start_time

    def set_next_move(self, move):
        self.next_move = move

    def is_collision(self, pos):
        return not (0 <= pos[0] < self.rows and 0 <= pos[1] < self.columns and self.grid[pos[0]][pos[1]] in [EMPTY_CHAR, FOOD_CHAR])

    def move_snake(self):
        if self.next_move is None or (self.previous_move is not None and (self.previous_move[0] + self.next_move[0], self.previous_move[1] + self.next_move[1]) == (0, 0)):
            self.next_move = self.previous_move
        if self.next_move is not None:
            head = self.snake[0]
            new_pos = (head[0] + self.next_move[0], head[1] + self.next_move[1])
            if self.is_collision(new_pos):
                self.alive = False
                if self.score > self.best_score:
                    self.best_score = self.score
            else:
                self.snake.insert(0, new_pos)
                self.grid[new_pos[0]][new_pos[1]] = SNAKE_CHAR
                if new_pos == self.food:
                    self.score += 1
                    self.spawn_food()
                else:
                    tail = self.snake.pop()
                    self.grid[tail[0]][tail[1]] = EMPTY_CHAR
                self.previous_move = self.next_move
                self.next_move = None

    def get_grid_base(self, width, height):
        menu_start = width * 2/3
        vertical_gap = (height - 1) // self.rows
        horizontal_gap = (menu_start - 1) // self.columns
        gap = min(horizontal_gap, vertical_gap)
        vertical_start = (height - self.rows * gap) // 2
        horizontal_start = (menu_start - self.columns * gap) // 2
        start = min(horizontal_start, vertical_start)
        return gap, vertical_start, horizontal_start, menu_start

    def get_coord(self, screen, pos):
        gap, vertical_start, horizontal_start, menu_start = self.get_grid_base(screen.get_width(), screen.get_height())
        x, y = pos
        i = int((y - vertical_start) // gap)
        j = int((x - horizontal_start) // gap)
        return i, j

    def add_wall(self, screen, pos):
        i, j = self.get_coord(screen, pos)
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.grid[i][j] = WALL_CHAR
        self.score = 0
        self.best_score = 0

    def remove(self, screen, pos):
        i, j = self.get_coord(screen, pos)
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.grid[i][j] = EMPTY_CHAR
        self.score = 0
        self.best_score = 0

    def draw_cells(self, screen, gap, vertical_start, horizontal_start):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i][j] != EMPTY_CHAR:
                    if self.grid[i][j] == WALL_CHAR:
                        color = WHITE
                    elif self.grid[i][j] == SNAKE_CHAR:
                        color = YELLOW
                    elif self.grid[i][j] == FOOD_CHAR:
                        color = RED
                    pygame.draw.rect(screen, color, (horizontal_start + j * gap, vertical_start + i * gap, gap, gap))


    def draw_grid(self, screen, gap, vertical_start, horizontal_start):
        for i in range(self.rows + 1):
            pygame.draw.line(screen, GREY, (horizontal_start, vertical_start + i * gap), (horizontal_start + self.columns * gap, vertical_start + i * gap), 1)
        for j in range(self.columns + 1):
            pygame.draw.line(screen, GREY, (horizontal_start + j * gap, vertical_start), (horizontal_start + j * gap, vertical_start + self.rows * gap), 1)

    def draw(self, screen, title_font, normal_font):
        screen.fill(BLACK)
        width, height = screen.get_size()
        gap, vertical_start, horizontal_start, menu_start = self.get_grid_base(width, height)
        self.draw_cells(screen, gap, vertical_start, horizontal_start)
        self.draw_grid(screen, gap, vertical_start, horizontal_start)
        pygame.draw.line(screen, GREY, (menu_start, 0), (menu_start, height))
        title = title_font.render(TITLE, True, WHITE)
        score = normal_font.render('Score: ' + str(self.score), True, WHITE)
        highscore = normal_font.render('Highscore: ' + str(self.best_score), True, WHITE)
        size = normal_font.render('Size: ' + str(self.rows) + 'x' + str(self.columns), True, WHITE)
        mps = normal_font.render('MPS: ' + str(self.mps), True, WHITE)
        start = title_font.render('Press Space', True, WHITE)
        if self.alive:
            self.current_time = time.time()
        timer = normal_font.render('Timer: ' + str(round(self.current_time - self.start_time, 1)), True, WHITE)
        screen.blit(title, (menu_start + (screen.get_width() - menu_start) / 2 - title.get_width() / 2, screen.get_height() * (1/15) - title.get_height()/2))
        screen.blit(score, (menu_start + (screen.get_width() - menu_start) / 7, screen.get_height() * (3/15) - score.get_height()/2 ))
        screen.blit(highscore, (menu_start + (screen.get_width() - menu_start) / 7, screen.get_height() * (4/15) - highscore.get_height()/2 ))
        screen.blit(size, (menu_start + (screen.get_width() - menu_start) / 7, screen.get_height() * (5/15) - size.get_height()/2))
        screen.blit(mps, (menu_start + (screen.get_width() - menu_start) / 7, screen.get_height() * (6/15) - mps.get_height()/2))
        if not self.alive:
            screen.blit(start, (menu_start + (width - menu_start) / 2 - start.get_width() / 2, height / 2 - start.get_height() / 2))
        screen.blit(timer, (menu_start + (screen.get_width() - menu_start) / 7, height - timer.get_height()))
        pygame.display.flip()

def main():
    #initializing pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((900, 600), pygame.RESIZABLE)
    pygame.display.set_caption(TITLE)
    title_font = pygame.font.Font('./Fonts/Mario-Kart-DS.ttf', 40)
    normal_font = pygame.font.Font('./Fonts/Fipps-Regular.otf', 20)
    clock = pygame.time.Clock()

    #initializing game
    game = Game()

    #game loop
    frame = 0
    while game.is_running():
        #triggering an event
        for event in pygame.event.get():
            #closing the game
            if event.type == pygame.QUIT:
                game.stop_running()
            elif event.type == pygame.KEYDOWN:
                if not game.is_alive():
                    #start the run
                    if event.key == pygame.K_SPACE:
                        game.start_run()

                    #modify speed
                    elif event.key == pygame.K_u:
                        game.slowdown()
                    elif event.key == pygame.K_i:
                        game.speedup()

                    #modify grid
                    elif event.key == pygame.K_r:
                        game.reset_grid()
                    elif event.key == pygame.K_o:
                        game.expand_row()
                    elif event.key == pygame.K_p:
                        game.expand_column()
                    elif event.key == pygame.K_l:
                        game.shrink_row()
                    elif event.key == pygame.K_SEMICOLON:
                        game.shrink_column()

                if game.is_alive():
                    #controls snake
                    if event.key == pygame.K_UP:
                        game.set_next_move(UP)
                    elif event.key == pygame.K_RIGHT:
                        game.set_next_move(RIGHT)
                    elif event.key == pygame.K_DOWN:
                        game.set_next_move(DOWN)
                    elif event.key == pygame.K_LEFT:
                        game.set_next_move(LEFT)

            #resize window
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                ratio = min(new_width/900, new_height/600)
                title_font = pygame.font.Font('./Fonts/Mario-Kart-DS.ttf', round(40 * ratio))
                normal_font = pygame.font.Font('./Fonts/Fipps-Regular.otf', round(20 * ratio))
            if not game.is_alive():
                #left click
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    game.add_wall(screen, pos)
                #right click
                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    game.remove(screen, pos)
        if game.is_alive() and frame/FPS >= 1/game.get_mps():
            game.move_snake()
            frame = 0
        #drawing on screen
        game.draw(screen, title_font, normal_font)
        clock.tick(FPS)
        frame = frame + 1
    pygame.font.quit()
    pygame.quit()

if __name__ == '__main__':
    main()
