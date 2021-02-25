import math
import pygame

def distance(x1, y1, x2, y2):
    distX = abs(x2 - x1)
    distY = abs(y2 - y1)
    return math.sqrt(distX ** 2 + distY ** 2)

def getClosest(rays):
    shortest = distance(rays[0].x, rays[0].y, rays[0].dx + rays[0].x, rays[0].dy + rays[0].y)
    for ray in rays:
        dist = distance(ray.x, ray.y, ray.dx + ray.x, ray.dy + ray.y)
        if dist < shortest:
            shortest = dist
    return shortest

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.deltaTheta = math.pi / 512
        self.angle = 0
        self.rays = []

    def display(self, world):
        pygame.draw.circle(world.screen, (255, 255, 255), (self.x, self.y), 5)
        for ray in self.rays:
            ray.display(world)

    def generateRays(self, obstacles):
        self.rays = []
        theta = self.angle
        while theta < self.angle + math.pi / 4:
            newRay = Ray(self.x, self.y, theta)
            newRay.calculateRay(obstacles)
            self.rays.append(newRay)
            theta += self.deltaTheta

    def render3D(self, world):
        world.render = []
        renderBG = Rectangle(1200, 300, 800, 600, (0, 0, 0))
        world.render.append(renderBG)

        
        for index, ray in enumerate(self.rays):
            rectWidth = 800 / len(self.rays)
            if index != len(self.rays) - 1:
                color = (math.sqrt(ray.dx ** 2 + ray.dy ** 2) - 
                         math.sqrt(self.rays[index + 1].dx ** 2 + self.rays[index + 1].dy ** 2))
                color += 10
                color *= 255 / 20

            length = math.sqrt(ray.dx ** 2 + ray.dy ** 2)
            if length < 1001 and length > 999:
                continue

            length = length * math.cos(ray.angle - self.angle + math.pi / 8)

            rectHeight = 600 - length

            if rectHeight < 0:
                rectHeight = 0
            
            if color > 255 or color < 0:
                rectColor = (0, 0, 0)
            else:
                rectColor = (255 - color, 255 - color, 255 - color)

            renderRect = Rectangle(800 + rectWidth/2 + rectWidth * index, 300, rectWidth + 2, rectHeight, rectColor)

            world.render.append(renderRect)


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def display(self, world):
        obstacle = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        pygame.draw.rect(world.screen, (255, 255, 255), obstacle, 1)

class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def display(self, world):
        rect = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        pygame.draw.rect(world.screen, self.color, rect, 0)

class Ray:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.angle = angle

    def display(self, world):
        pygame.draw.line(world.screen, (255, 255, 255), (self.x, self.y), (self.x + self.dx, self.y + self.dy))

    def calculateRay(self, obstacles):
        """
        checks if ray intersects with list of obstacles
        args:
            obstacles (Obstacle[]): list of obstacles
        returns:
            Point: point of nearest intersection
        """
        intersections = []

        for obstacle in obstacles:
            POI = self.pointOfIntersection(obstacle)
            if POI != None:
                intersections.append(POI)
        
        if len(intersections) == 0:
            self.dx = 1000 * math.cos(self.angle)
            self.dy = 1000 * math.sin(self.angle)
        else:
            minDistance = self.closestPoint(intersections)
            self.dx = minDistance * math.cos(self.angle)
            self.dy = minDistance * math.sin(self.angle)

    
    def pointOfIntersection(self, rect):
        deltaX = rect.x - self.x
        deltaY = rect.y - self.y

        if deltaY == 0:
            y1 = self.y
        else:
            y1 = rect.y - (deltaY / abs(deltaY)) * rect.height/2
        if math.sin(self.angle) == 0:
            x1 = self.x
        else:
            x1 = (y1 - self.y) * (math.cos(self.angle) / math.sin(self.angle)) + self.x

        if deltaX == 0:
            x2 = self.x
        else:
            x2 = rect.x - (deltaX / abs(deltaX)) * rect.width/2
        if math.cos(self.angle) == 0:
            y2 = 0
        else:
            y2 = (x2 - self.x) * math.tan(self.angle) + self.y

        if (abs(x1 - rect.x) < rect.width/2) and math.sin(self.angle) * (y1 - self.y) > 0:
            if (abs(y2 - rect.y) < rect.height/2) and math.cos(self.angle) * (x2 - self.x) > 0:
                dist1 = distance(x1, y1, self.x, self.y)
                dist2 = distance(x2, y2, self.x, self.y)
                if dist1 < dist2:
                    return (x1, y1)
                return (x2, y2)
            return (x1, y1)
        elif (abs(y2 - rect.y) < rect.height/2) and math.cos(self.angle) * (x2 - self.x) > 0:
                return (x2, y2)
        return None

    def closestPoint(self, points):
        minDistance = distance(self.x, self.y, points[0][0], points[0][1])
        closestPoint = points[0]
        for i in range(1, len(points)):
            dist = distance(self.x, self.y, points[i][0], points[i][1])

            if (dist < minDistance):
                closestPoint = points[i]
                minDistance = dist
        
        return minDistance 





    

