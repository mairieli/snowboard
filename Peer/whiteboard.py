import pygame

class Whiteboard:

    def __init__(self, my_color, queue_receiver, queue_sender):
        self.screen = pygame.display.set_mode((640, 480))
        self.clicked = False;
        self.points = []
        self.screen.fill((255,255,255))
        self.queue_receiver = queue_receiver
        self.queue_sender = queue_sender
        self.my_color = my_color

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

                if event.type == pygame.MOUSEMOTION and self.clicked:
                    point = event.__dict__['pos']
                    self.points.append(point)
                    queue_sender(str(self.my_color[0]) + ":" str(self.my_color[1]) + ":" str(self.my_color[2]) + ":" + str(point[0]) + ":" + str(point[1]))

                if event.type == pygame.MOUSEBUTTONUP:
                    queue_sender(str(self.my_color[0]) + ":" str(self.my_color[1]) + ":" str(self.my_color[2]) + ":x")
                    self.clicked = False
                    self.points = []

                if len(self.points) >= 2:
                    pygame.draw.aalines(self.screen, self.my_color, False, [self.points[0], self.points[1]])
                    self.points.remove(self.points[0])

                for color, color_points in self.queue_receiver.items():
                    if len(color_points) >= 2:
                        if color_points[1] == "x":
                            self.points.remove(self.points[0])
                        else:
                            pygame.draw.aalines(self.screen, color, False, [color_points[0], color_points[1]])
                            color_points.remove(color_points[0])

                pygame.display.flip()