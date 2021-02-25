import pygame
import math
from player import Player
from player import Obstacle

def main():
    pygame.init()

    world = World([1600, 600])

    player = Player(500, 300)
    obstacle = Obstacle(300, 100, 200, 100)
    obstacle2 = Obstacle(700, 500, 100, 200)
    obstacle3 = Obstacle(300, 500, 400, 100)
    world.nodes.append(player)
    world.nodes.append(obstacle)
    world.nodes.append(obstacle2)
    world.nodes.append(obstacle3)

    running = True
    pressedUP = False
    pressedDOWN = False
    pressedLEFT = False
    pressedRIGHT = False
    pressedR = False
    pressedLSHIFT = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pressedUP = True
                if event.key == pygame.K_DOWN:
                    pressedDOWN = True
                if event.key == pygame.K_LEFT:
                    pressedLEFT = True
                if event.key == pygame.K_RIGHT:
                    pressedRIGHT = True
                if event.key == pygame.K_r:
                    pressedR = True
                if event.key == pygame.K_LSHIFT:
                    pressedLSHIFT = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pressedUP = False
                if event.key == pygame.K_DOWN:
                    pressedDOWN = False
                if event.key == pygame.K_LEFT:
                    pressedLEFT = False
                if event.key == pygame.K_RIGHT:
                    pressedRIGHT = False
                if event.key == pygame.K_r:
                    pressedR = False
                if event.key == pygame.K_LSHIFT:
                    pressedLSHIFT = False
    
        if pressedUP:
            player.y -= 2
        if pressedDOWN:
            player.y += 2
        if pressedLEFT:
            player.x -= 2
        if pressedRIGHT:
            player.x += 2
        if pressedR and pressedLSHIFT:
            player.angle = (player.angle - player.deltaTheta) % (2 * math.pi)
        elif pressedR:
            player.angle = (player.angle + player.deltaTheta) % (2 * math.pi)

        world.nodes[0].generateRays(world.nodes[1:])

        world.update()


class World:
    def __init__(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.fps = 240
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps)
        self.nodes = []
        self.render = []

    def update(self):
        self.screen.fill((0, 0, 0))

        for node in self.nodes:
            node.display(self)

        self.nodes[0].render3D(self)

        for rect in self.render:
            rect.display(self)
        
        pygame.display.flip()


if __name__ == "__main__":
    main()
