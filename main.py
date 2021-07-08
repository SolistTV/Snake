from tkinter import Tk, Canvas
import random

# Globals
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


def create_block():
    """ Create block """
    global BLOCK
    position_x = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
    position_y = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))
    # блок это кружочек красного цвета
    BLOCK = canvas.create_oval(position_x, position_y, position_x + SEG_SIZE, position_y + SEG_SIZE, fill="#22ff3d")


# main function run game
def main():
    global IN_GAME
    if IN_GAME:
        # Двигаем змейку
        snake.move()
        # Определяем координаты головы
        head_coordinates = canvas.coords(snake.segments[-1].instance)
        x1, y1, x2, y2 = head_coordinates
        # Столкновение с границами экрана
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Поедание яблок
        elif head_coordinates == canvas.coords(BLOCK):
            snake.add_segment()
            canvas.delete(BLOCK)
            create_block()

        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(snake.segments) - 1):
                if canvas.coords(snake.segments[index].instance) == head_coordinates:
                    IN_GAME = False
        root.after(100, main)

    # Если не в игре выводим сообщение о проигрыше
    else:
        canvas.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER!", font="Arial 20", fill="#ff0000")


# Segments class
class Segment(object):
    def __init__(self, x, y):
        self.instance = canvas.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="#001ead")


# Snake class
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # directions
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}
        # start direction
        self.vector = self.mapping["Right"]

    def move(self):
        """Move snake with direction"""
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = canvas.coords(self.segments[index + 1].instance)
            # set segments positions
            canvas.coords(segment, x1, y1, x2, y2)
            # get coordinates of segments
            x1, y1, x2, y2 = canvas.coords(self.segments[-2].instance)
            # put head by move direction
            canvas.coords(
                self.segments[-1].instance,
                x1 + self.vector[0] * SEG_SIZE,
                y1 + self.vector[1] * SEG_SIZE,
                x2 + self.vector[0] * SEG_SIZE,
                y2 + self.vector[1] * SEG_SIZE
            )

    def change_direction(self, event):
        """ Change move direction """

        # event pressed key
        # if pressed key have direction change direction
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        """ Add segment to snake """

        # get last segment
        last_seg = canvas.coords(self.segments[0].instance)
        # get direction coordinates
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE

        # add segment to snake by direction
        self.segments.insert(0, Segment(x, y))


# create window
root = Tk()
# name window
root.title("Snake")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="#a4eacd")
canvas.grid()
canvas.focus_set()
# создаем набор сегментов
segments = [
    Segment(SEG_SIZE, SEG_SIZE),
    Segment(SEG_SIZE * 2, SEG_SIZE),
    Segment(SEG_SIZE * 3, SEG_SIZE)
]

# create first block
create_block()
# собственно змейка
snake = Snake(segments)
canvas.bind("<KeyPress>", snake.change_direction)
# run game
main()
# run window
root.mainloop()
