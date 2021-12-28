"""
Tiles
History

17-Jul-2021 - Initial version-controlled code for tile generation and management. 
 Note: walls now changes to access with opposite truth values.
"""
import random
import pygame


class Tile:
    """
    Represents a tile in the Shifting Maze game, including image of tile.

    Attributes:
        number : int
            Unique number assigned to tile
        doors : list
            List of values representing no door or blank wall (0) or a door (1).
            These proceed anti-clockwise from up the screen. Default: [1,1,1,1]
        size : integer
            Length of one edge of a square tile, including frame. Default: 102
        frame : int
            Width of frame around edge of tile. Default: 1
        wall_width : int
            Thickness of walls. Default: 10
        door_width : int
            Width of doorways. Default: 50
        image : pygame.Surface
            Image of tile
        rect : pygame.Surface.rect
            Rectangle describing tile image
        frame_colour : tuple
            Red, green, blue tuple for colour of frame around tile.
            Default: (192, 192, 192) = LIGHT_GREY
        wall_colour : tuple
            Red, green, blue tuple for colour of walls
            Default: (200, 100, 100) = RED
        floor_colour : tuple
            Red, green, blue tuple for colour of floor.
            Default: (150, 150, 255) # BLUE
    """

    def __init__(self, number, doors=[1, 1, 1, 1]):
        """
        Parameters:
            number : int
                Unique number assigned to tile
            doors : list
                List of values representing no door or blank wall (0) or a door (1).
                These proceed anti-clockwise from up the screen. Default: [1,1,1,1]
        """
        self.number = number
        self.doors = doors

        self.size = 102
        self.frame = 1
        self.wall_width = 10
        self.door_width = 50

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        self.frame_colour = (192, 192, 192)  # LIGHT_GREY
        self.rect = self.image.get_rect()
        self.image.fill(self.frame_colour)

        self.wall_colour = (200, 100, 100)  # RED
        self.full_rect = (
            self.frame,
            self.frame,
            self.size - 2 * self.frame,
            self.size - 2 * self.frame,
        )
        pygame.draw.rect(self.image, self.wall_colour, self.full_rect)

        self.floor_colour = (150, 150, 255)  # BLUE
        self.floor_rect = (
            self.frame + self.wall_width,
            self.frame + self.wall_width,
            self.size - 2 * (self.frame + self.wall_width),
            self.size - 2 * (self.frame + self.wall_width),
        )
        pygame.draw.rect(self.image, self.floor_colour, self.floor_rect)

        if doors[0]:
            self.top_door_rect = (
                int((self.size - self.door_width) / 2),
                self.frame,
                self.door_width,
                self.wall_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.top_door_rect)

        if doors[1]:
            self.left_door_rect = (
                self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.left_door_rect)

        if doors[2]:
            self.bottom_door_rect = (
                int((self.size - self.door_width) / 2),
                self.size - self.wall_width - self.frame,
                self.door_width,
                self.wall_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.bottom_door_rect)

        if doors[3]:
            self.right_door_rect = (
                self.size - self.wall_width - self.frame,
                int((self.size - self.door_width) / 2),
                self.wall_width,
                self.door_width,
            )
            pygame.draw.rect(self.image, self.floor_colour, self.right_door_rect)


class TileSet:
    """
    Represents a set of tiles for use in the Shifting Maze game.

    Attributes
        name : string
            Name of tile set. Default: "standard".
        tiles : dict
            Dictionary of tiles indexed by the tile number.
        tile_counts : int
            Number of each tile in set.
    """

    def __init__(self, doors_for_tiles, tile_counts, name="standard"):
        """
        Parameters
            name : string
                Name of tile set. Default: "standard"
            doors_for_tiles : dict
                Dictionary with lists of doors for each tile.
                Each list represents no door or blank wall (0) or a door (1) for each side.
                These proceed anti-clockwise from up the screen.
            tile_counts : dict
                Dictionary with then number of each tile in set.
        """
        self.name = name
        self.tile_counts = tile_counts
        self.different_tiles = len(tile_counts)
        self.tiles = {}
        for tile_number, doors in doors_for_tiles.items():
            self.tiles[tile_number] = Tile(tile_number, doors)

    def __str__(self):
        """Print set of tiles"""
        string = f"Tile set: {self.name}\n"
        for number in range(self.different_tiles):
            string += f" {number}:{self.tiles[number].doors}\n"
        return string


class TileBag:
    """
    Represents the bag of tiles from which random ones can be drawn for the Shifting Maze game.

    Attributes
        tile_numbers : list
            List of the tiles in the bag in a random order
    """

    def __init__(self, tile_set):
        """
        Parameters
            tile_set : TileSet
                Set of tiles in play for a game of the Shifting Maze.
        """
        self.tile_numbers = []
        for tile_number, tile_count in tile_set.tile_counts.items():
            self.tile_numbers += [tile_number] * tile_count
        self.mix()

    def mix(self):
        """Mix the content of the bag"""
        random.shuffle(self.tile_numbers)

    def draw_tile(self):
        """
        Draw a single tile from the bag

        Parameters
            none

        Returns
            tile_number : int
                Number of tile drawn
        """
        return self.tile_numbers.pop()

    def draw_tiles(self, number=1):
        """
        Draw a number tiles from the bag

        Parameters
            number : int
                Number of tiles to be drawn. Default = 1

        Returns
            tile_list : list
                List of the tiles
        """
        tile_list = []
        for n in range(number):
            tile_list.append(self.draw_tile())
        return tile_list

    def return_tile(self, tile_number):
        """
        Return a single tile to the bag and shuffle

        Parameters
            tile_number : int
                Number of tile drawn
        """
        self.tile_numbers.append(tile_number)
        self.mix()

    def __repr__(self):
        """Display tile bag"""
        tile_list = ""
        for tile_number in self.tile_numbers:
            tile_list += str(tile_number) + " "
        return tile_list

    def __str__(self):
        """Print tile bag"""
        tile_list = ""
        for tile_number in self.tile_numbers:
            tile_list += str(tile_number) + " "
        return tile_list