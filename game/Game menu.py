import pytmx
import pygame

def load_tilemap(map_file):
    """Loads a tilemap file and returns a list of collision tiles."""
    # Load the tilemap
    tilemap = pytmx.load_pygame(map_file)

    collision_tiles = []  # To store rectangles of solid tiles

    # Iterate through layers and collect collidable tiles
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):  # Ensure it's a tile layer
            for x, y, gid in layer:  # Iterate over tile grid
                # Retrieve the tile object using the GID (Global ID)
                tile = tilemap.get_tile_properties_by_gid(gid)
                if tile and "collidable" in tile:  # Check if "collidable" property exists
                    collision_tiles.append(pygame.Rect(
                        x * tilemap.tilewidth,
                        y * tilemap.tileheight,
                        tilemap.tilewidth,
                        tilemap.tileheight
                    ))

    return tilemap, collision_tiles
