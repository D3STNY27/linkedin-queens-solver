def index_to_coordinate(index: int, cols: int) -> tuple:
    return (index // cols), (index % cols)


def coordinate_to_index(coordinate: tuple, cols: int) -> int:
    x, y = coordinate
    return x * cols + y
