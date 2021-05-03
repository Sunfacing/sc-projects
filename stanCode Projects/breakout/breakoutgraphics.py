"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This class provides attributes of Ball / Bricks / Paddle
and necessary methods that help run the game
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

# CONSTANT for creating Bricks / Paddle / Balls / Ball's Speed
BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10       # Number of rows of bricks.
BRICK_COLS = 10       # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75     # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
INITIAL_Y_SPEED = 3    # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

# global variables for creating bricks
ball_color = ['red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'blue', 'blue']
ball_color_index = 0  # The index of ball_color
brick_x = 0
brick_y = 0


class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):
        """Create a window with bricks, a paddle, a ball and its speed"""
        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width - paddle_width) / 2, y=window_height - paddle_offset)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle.color = 'black'
        self.window.add(self.paddle)
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius * 2, ball_radius * 2, x=(window_width - ball_radius) / 2, y=(window_height - ball_radius) / 2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball)
        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.__dy = INITIAL_Y_SPEED

        # Initialize our mouse listeners
        self.game_on = False
        onmouseclicked(self.game_initiated)
        onmousemoved(self.paddle_position)

        # Draw bricks
        global brick_x, brick_y, ball_color_index
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.brick.fill_color = ball_color[ball_color_index]
                self.brick.color = ball_color[ball_color_index]
                self.window.add(self.brick, x=brick_x, y=brick_y)
                brick_x = brick_x + brick_width + brick_spacing
            ball_color_index += 1
            brick_x = 0
            brick_y = brick_y + brick_height + brick_spacing

        # Total number of bricks used for counting how many bricks player should remove
        self.brick_number = brick_rows * brick_cols

    def paddle_position(self, mouse):
        """Set the paddle's position"""
        if self.paddle.width / 2 <= mouse.x <= self.window.width - self.paddle.width / 2:
            self.paddle.x = mouse.x - self.paddle.width / 2
        self.paddle.y = self.window.height - BRICK_OFFSET

    def game_initiated(self, mouse):
        """Check if game starts and used for preventing onmouseclicked() function"""
        self.game_on = True

    def dx_getter(self):
        """Get the ball's horizontal speed"""
        return self.__dx

    def dy_getter(self):
        """Get the ball's vertical speed"""
        return self.__dy

    def reset_ball(self):
        """Everytime the ball falls under the bottom the the screen, it will spawn at the original place"""
        self.ball.x = (self.window.width - BALL_RADIUS) / 2
        self.ball.y = (self.window.height - BALL_RADIUS) / 2
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.__dy = INITIAL_Y_SPEED

    def brick_detect(self):
        """Use 4 angles of the ball to detect if touching an object"""
        detector_upper_left = self.window.get_object_at(self.ball.x, self.ball.y)
        detector_upper_right = self.window.get_object_at(self.ball.x + BALL_RADIUS * 2, self.ball.y)
        detector_lower_left = self.window.get_object_at(self.ball.x, self.ball.y + BALL_RADIUS * 2)
        detector_lower_right = self.window.get_object_at(self.ball.x + BALL_RADIUS * 2, self.ball.y + BALL_RADIUS * 2)
        if detector_upper_left is not None:
            if detector_upper_left is self.paddle:
                return 0
            else:
                self.window.remove(detector_upper_left)
                return True
        elif detector_upper_right is not None:
            if detector_upper_right is self.paddle:
                return 0
            else:
                self.window.remove(detector_upper_right)
                return True
        elif detector_lower_left is not None:
            if detector_lower_left is self.paddle:
                return 0
            else:
                self.window.remove(detector_lower_left)
                return True
        elif detector_lower_right is not None:
            if detector_lower_right is self.paddle:
                return 0
            else:
                self.window.remove(detector_lower_right)
                return True

    def game_winning_screen(self, width=BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING, height=BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)):
        """Show "You Win!!" after successfully removing all bricks"""
        game_winning_screen = GRect(width, height)
        game_winning_screen.filled = True
        game_winning_screen.fill_color = 'white'
        game_winning_screen.color = 'white'
        self.window.add(game_winning_screen)
        game_winning_text = GLabel('You Win!!')
        game_winning_text.font = 'Helvetica' + '-' + str(BRICK_COLS * 5)
        self.window.add(game_winning_text, (width - game_winning_text.width) / 2, height / 2)

    def game_over_screen(self, width=BRICK_COLS * (BRICK_WIDTH + BRICK_SPACING) - BRICK_SPACING, height=BRICK_OFFSET + 3 * (BRICK_ROWS * (BRICK_HEIGHT + BRICK_SPACING) - BRICK_SPACING)):
        """Show "Game Over" if player runs out of lives"""
        game_over_background = GRect(width, height)
        game_over_background.filled = True
        game_over_background.fill_color = 'white'
        game_over_background.color = 'white'
        self.window.add(game_over_background)
        game_over_text = GLabel('Game Over')
        game_over_text.font = 'Helvetica' + '-' + str(BRICK_COLS * 5)
        self.window.add(game_over_text, (width - game_over_text.width) / 2, height / 2)