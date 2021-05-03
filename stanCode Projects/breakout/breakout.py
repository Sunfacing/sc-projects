"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This program creates a breakout game, which sets a certain number of bricks
that player has to hits by a ball with a paddle, the game stops only when
the bricks are all remvoed or player runs out of lives, which is 3.
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics


FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    TODO: When clicking mouse, the ball starts to move, this program will counts bricks removed and the lives player still has
          if all bricks removed or player's lives = 0, the screen shows up a 'Game Over' or 'You Win' message
    """
    num_death = 0
    graphics = BreakoutGraphics()
    bricks_left = graphics.brick_number
    x = graphics.dx_getter()
    y = graphics.dy_getter()
    while True:
        # Check if player removes all the bricks
        if bricks_left == 0:
            graphics.game_winning_screen()
            break
        if graphics.game_on:
            graphics.ball.move(x, y)
            # Count Scores and Remove Bricks, sometimes graphics.brick_detect() hits 3 bricks at the sametime, but bricks_left only counts 1, so do 3 times of counting
            if graphics.brick_detect():
                bricks_left -= 1
                if graphics.brick_detect():
                    bricks_left -= 1
                    if graphics.brick_detect():
                        bricks_left -= 1
                y = -y

            # Detect if the ball hits the paddle, ignore if paddle hits the ball from two sides
            # The 3rd condition: graphics.paddle.y ...... graphics.paddle.y can make ball bounce only when is at the upper half side, and prevent ball from boucing when already at the bottom of the paddle
            if graphics.brick_detect() == 0 and graphics.paddle.y + graphics.paddle.height / 1.3 >= graphics.ball.y + graphics.ball.height >= graphics.paddle.y:
                y = -abs(y)

            # Detect if the ball hits the wall
            if graphics.ball.x <= 0 or graphics.ball.x >= graphics.window.width:
                x = -x
            if graphics.ball.y <= 0:
                y = -y

            # Detect if the ball reaches the bottom and check number of life left
            if graphics.ball.y >= graphics.window.height:
                num_death += 1
                if num_death < NUM_LIVES:
                    graphics.reset_ball()
                    x = graphics.dx_getter()
                    y = graphics.dy_getter()
                    graphics.game_on = False
                else:
                    graphics.game_over_screen()
                    break
            pause(FRAME_RATE)
        else:
            # Keep ball staying at the same place
            graphics.ball.move(0, 0)
            pause(FRAME_RATE)



if __name__ == '__main__':
    main()
