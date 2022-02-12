"""
Remi Coding
Draw Koch Fractals using Generative Recursion from How to Code: Complex Data
Edx
"""

# Imports
import turtle


def pen_position(pen, x_pos, y_pos):
    """
    Move the pen to the specified x and y positions on the Python Turtle Graphics

    Arguments:
    `pen`: turtle object
    `x_pos`: int that represents the x position on the Python Turtle Graphics
    `y_pos`: int that represents the y position on the Python Turtle Graphics
    """
    pen.up()
    pen.goto(x_pos, y_pos)
    pen.down()


def snowflake(pen, turn):
    """
    Helper function that defines parameters for the Koch snowflake fractals specifically

    Arguments:
    `pen`: turtle object
    `turn`: int representing a categorical variable (1, 2) that select the angle that the turtle turns
    """
    if turn == 1:
        pen.rt(60)
    else:
        pen.lt(120)


def anti_snowflake(pen, turn):
    """
    Helper function that defines parameters for the Koch antisnowflake fractals specifically

    Arguments:
    `pen`: turtle object
    `turn`: int representing a categorical variable (1, 2) that select the angle that the turtle turns
    """
    if turn == 1:
        pen.lt(60)
    else:
        pen.rt(120)


def koch_triangular(pen, distance, figure_side, shape):
    """
    Draw shapes on one side of the triangular shaped Koch fractal

    Arguments:
    `pen`: turtle object
    `distance`: int representing the length of the side
    `figure_side`: int representing the number of sides of the shape
    `shape`: function named after the type of Koch fractal to be drawn
    """
    if distance < 10:
        pen.fd(distance)
        return

    new_distance = distance / figure_side

    koch_triangular(pen, new_distance, figure_side, shape)
    shape(pen, 1)
    koch_triangular(pen, new_distance, figure_side, shape)
    shape(pen, 2)
    koch_triangular(pen, new_distance, figure_side, shape)
    shape(pen, 1)
    koch_triangular(pen, new_distance, figure_side, shape)


def draw_koch(pen, distance, figure_side, shape):
    """
    Draw specified Koch fractal shape

    Arguments:
    `pen`: turtle object
    `distance`: int representing the length of the side
    `figure_side`: int representing the number of sides of the shape
    `shape`: function named after the type of Koch fractal to be drawn
    """
    for i in range(figure_side):
        koch_triangular(pen, distance, figure_side, shape)
        if figure_side == 3:
            pen.lt(120)
        else:
            pen.lt(90)


def main():
    pen = turtle.Turtle()

    triangle_distance = 297
    quadratic_distance = 800

    triangular_side = 3
    quadratic_side = 4

    pen.speed(0)

    # Drawing Koch Snowflake Fractal
    pen_position(pen, -600, -100)
    draw_koch(pen, triangle_distance, triangular_side, snowflake)

    # Drawing Koch Antisnowflake Fractal
    pen_position(pen, -285, -100)
    draw_koch(pen, triangle_distance, triangular_side, anti_snowflake)

    # Drawing Cesaro Antisnowflake Fractal
    # A variant of the Koch Antisnowflake with an angle between 60° and 90°
    pen_position(pen, 25, -100)
    draw_koch(pen, quadratic_distance, quadratic_side, anti_snowflake)

    turtle.done()


if __name__ == "__main__":
    main()
