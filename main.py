import turtle
import math


SCREEN_SIZE = (800, 400)
TITLE_BBOX = ((-300, 170), (300, 150))
WORLD_BBOX = ((-380, 130), (-10, -150))
VIEW_BBOX = ((10, 130), (380, -150))


COLORS = {
    0: "AliceBlue",
    1: "Cyan4",
    2: "DarkRed",
    3: "DarkSlateGrey",
    4: "azure4"
}

MAP = [
    [1,1,1,1,1,1],
    [1,0,0,0,0,2],
    [2,2,0,0,2,2],
    [1,0,0,0,0,2],
    [1,1,1,1,1,1]
]

PLAYER_POS = (3.5, 1.5)
PLAYER_DIR = 30 #degrees

def draw_rectangle(bbox: tuple[tuple[int]]) -> None:
    turtle.penup()
    turtle.goto(bbox[0])
    turtle.setheading(0)
    turtle.pendown()

    width = bbox[1][0] - bbox[0][0]
    height = bbox[0][1] - bbox [1][1]

    for i in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)

def draw_world() -> None:
    for i, row in enumerate(MAP):
        for j, tile in enumerate(row):
            draw_cell(i, j, tile)
    
    draw_dot(*PLAYER_POS, "Red", 16)

def draw_dot(i: int, j: int, color: str, radius: int) -> None:
    center = cell_to_pixel(i, j)
    turtle.fillcolor(color)
    turtle.begin_fill()

    turtle.penup()
    turtle.goto(center[0], center[1] - radius)
    turtle.setheading(0)

    turtle.pendown()
    turtle.circle(radius)
    turtle.end_fill()


def draw_cell(i: int, j: int, tile: int) -> None:
    cell_bbox = get_bbox(i, j)
    turtle.fillcolor(COLORS[tile])
    turtle.begin_fill()
    draw_rectangle(cell_bbox)
    turtle.end_fill()

def get_bbox(i: int, j: int) -> tuple[tuple[int]]:
    return (cell_to_pixel(i, j), cell_to_pixel(i+1, j+1))

def cell_to_pixel(i: int, j: int) -> tuple[int]:
    cell_width = (WORLD_BBOX[1][0] - WORLD_BBOX[0][0]) / len(MAP[0])
    cell_height = (WORLD_BBOX[0][1] - WORLD_BBOX[1][1]) / len(MAP)
    start_x = WORLD_BBOX[0][0]
    start_y  = WORLD_BBOX[0][1]
    x = start_x + j * cell_width
    y = start_y - i * cell_height
    
    return (x,y)

def perform_raycast() -> None:
    ray_y, ray_x = PLAYER_POS
    dx = math.cos(math.radians(PLAYER_DIR))
    dy = -math.sin(math.radians(PLAYER_DIR))

    screen_width = VIEW_BBOX[1][0] - VIEW_BBOX[0][0]
    view_left_x = VIEW_BBOX[0][0]
    view_top_y = VIEW_BBOX[0][1]
    view_bottom_y = VIEW_BBOX[1][1]
    view_center_y = (view_top_y + view_bottom_y) / 2

    for i in range(screen_width):
        horizontal_coefficient = i / (screen_width / 2) - 1
        ray_dx = dx - horizontal_coefficient * dy
        ray_dy = dy + horizontal_coefficient * dx


        delta_x = 1e30 if ray_dx == 0 else 1 / abs(ray_dx)
        delta_y = 1e30 if ray_dy == 0 else 1 / abs(ray_dy)

        map_x = int(ray_x)
        map_y = int(ray_y)

        side_dixt_x = 0.0
        side_dist_y = 0.0
        step_x = 0
        step_y = 0

        if (ray_dx < 0):
            step_x = -1
            side_dist_x = (ray_x - map_x) * delta_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1 - ray_x) * delta_x
        if (ray_dy < 0):
            step_y = -1
            side_dist_y = (ray_y - map_y) * delta_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1 - ray_y) * delta_y
        
        hit = False
        side = 0 # vert is 0, horizontal is 1
        while not hit:
            if side_dist_x < side_dist_y:
                x = ray_x + side_dist_x * ray_dx
                y = ray_y + side_dist_x * ray_dy

                side_dist_x += delta_x
                map_x += step_x
                side = 0
            else:
                x = ray_x + side_dist_y * ray_dx
                y = ray_y + side_dist_y * ray_dy

                side_dist_y += delta_y
                map_y += step_y
                side = 1

            if (MAP[map_y][map_x] != 0):
                hit = True
        
        depth = side_dist_y - delta_y
        if(side == 0):
            depth = side_dist_x - delta_x
        
        wall_top = min(view_top_y, (view_center_y + 64) / depth)
        wall_bot = max(view_bottom_y, (view_center_y - 64) / depth)

        # ceiling
        turtle.penup()
        turtle.goto(view_left_x + i, view_top_y)
        turtle.pendown()
        turtle.pencolor(COLORS[3])
        turtle.goto(view_left_x + i, wall_top)

        # wall
        turtle.penup()
        turtle.goto(view_left_x + i, wall_top)
        turtle.pendown()
        turtle.pencolor(COLORS[MAP[map_y][map_x]])
        turtle.goto(view_left_x + i, wall_bot)

        # floor
        turtle.penup()
        turtle.goto(view_left_x + i, wall_bot)
        turtle.pendown()
        turtle.pencolor(COLORS[4])
        turtle.goto(view_left_x + i, view_bottom_y)

def visualize_raycast() -> None:
    ray_y, ray_x = PLAYER_POS
    ray_dx = math.cos(math.radians(PLAYER_DIR))
    ray_dy = -math.sin(math.radians(PLAYER_DIR))
    delta_x = 1e30 if ray_dx == 0 else 1 / abs(ray_dx)
    delta_y = 1e30 if ray_dy == 0 else 1 / abs(ray_dy)

    map_x = int(ray_x)
    map_y = int(ray_y)

    side_dixt_x = 0.0
    side_dist_y = 0.0
    step_x = 0
    step_y = 0

    if (ray_dx < 0):
        step_x = -1
        side_dist_x = (ray_x - map_x) * delta_x
    else:
        step_x = 1
        side_dist_x = (map_x + 1 - ray_x) * delta_x
    if (ray_dy < 0):
        step_y = -1
        side_dist_y = (ray_y - map_y) * delta_y
    else:
        step_y = 1
        side_dist_y = (map_y + 1 - ray_y) * delta_x
    
    hit = False
    side = 0 # vert is 0, horizontal is 1
    while not hit:
        if side_dist_x < side_dist_y:
            x = ray_x + side_dist_x * ray_dx
            y = ray_y + side_dist_x * ray_dy
            draw_dot(y, x, "Black", 4)

            side_dist_x += delta_x
            map_x += step_x
            side = 0
        else:
            x = ray_x + side_dist_y * ray_dx
            y = ray_y + side_dist_y * ray_dy
            draw_dot(y, x, "Black", 4)

            side_dist_y += delta_y
            map_y += step_y
            side = 1

        if (MAP[map_y][map_x] != 0):
            hit = True
    
    depth = min(side_dist_y, side_dist_x)
    x = ray_x + depth * ray_dx
    y = ray_y + depth * ray_dy
    turtle.penup()
    turtle.goto(cell_to_pixel(ray_y, ray_x))
    turtle.pendown()
    turtle.goto(cell_to_pixel(y, x))

if __name__ == '__main__':
    turtle.setup(*SCREEN_SIZE)
    turtle.hideturtle()
    turtle.speed(0)
    draw_rectangle(TITLE_BBOX)
    draw_rectangle(WORLD_BBOX)
    draw_rectangle(VIEW_BBOX)
    draw_world()
    visualize_raycast()
    perform_raycast()
    turtle.done()

