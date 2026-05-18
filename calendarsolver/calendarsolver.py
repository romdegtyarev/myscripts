#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterator


Coord = tuple[int, int]
Shape = tuple[Coord, ...]

@dataclass(frozen=True)
class Piece:
    name: str
    cells: Shape


MONTHS = {
    1: "ЯНВ",
    2: "ФЕВ",
    3: "МАР",
    4: "АПР",
    5: "МАЙ",
    6: "ИЮН",
    7: "ИЮЛ",
    8: "АВГ",
    9: "СЕН",
    10: "ОКТ",
    11: "НОЯ",
    12: "ДЕК",
}

WEEKDAYS = {
    0: "ПН",
    1: "ВТ",
    2: "СР",
    3: "ЧТ",
    4: "ПТ",
    5: "СБ",
    6: "ВС",
}


BLACK: set[Coord] = {
    (0, 6),
    (1, 6),
    (7, 0),
    (7, 1),
    (7, 2),
    (7, 3),
}

BOARDLABELS: dict[Coord, str] = {
    (0, 0): "ЯНВ", (0, 1): "ФЕВ", (0, 2): "МАР", (0, 3): "АПР", (0, 4): "МАЙ", (0, 5): "ИЮН",
    (1, 0): "ИЮЛ", (1, 1): "АВГ", (1, 2): "СЕН", (1, 3): "ОКТ", (1, 4): "НОЯ", (1, 5): "ДЕК",

    (2, 0): "1",  (2, 1): "2",  (2, 2): "3",  (2, 3): "4",  (2, 4): "5",  (2, 5): "6",  (2, 6): "7",
    (3, 0): "8",  (3, 1): "9",  (3, 2): "10", (3, 3): "11", (3, 4): "12", (3, 5): "13", (3, 6): "14",
    (4, 0): "15", (4, 1): "16", (4, 2): "17", (4, 3): "18", (4, 4): "19", (4, 5): "20", (4, 6): "21",
    (5, 0): "22", (5, 1): "23", (5, 2): "24", (5, 3): "25", (5, 4): "26", (5, 5): "27", (5, 6): "28",

    (6, 0): "29", (6, 1): "30", (6, 2): "31", (6, 3): "ПН", (6, 4): "ВТ", (6, 5): "СР", (6, 6): "ЧТ",
    (7, 4): "ПТ", (7, 5): "СБ", (7, 6): "ВС",
}

PLAYABLELABELS: set[Coord] = set(BOARDLABELS) - BLACK

PIECES: tuple[Piece, ...] = (
    Piece("🟥", ((0, 0), (1, 0), (2, 0), (2, 1))),
    Piece("🟧", ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1))),
    Piece("🟨", ((0, 0), (1, 0), (2, 0), (3, 0))),
    Piece("🟩", ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))),
    Piece("🟦", ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))),
    Piece("🟪", ((0, 0), (0, 1), (1, 0), (2, 0), (2, 1))),
    Piece("🔳", ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0))),
    Piece("🔲", ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2))),
    Piece("🟫", ((0, 0), (1, 0), (1, 1), (2, 1))),
    Piece("❎", ((0, 0), (1, 0), (2, 0), (2, 1), (3, 1))),
)

PIECES_: tuple[Piece, ...] = (
    Piece("A", ((0, 0), (1, 0), (2, 0), (2, 1))),
    Piece("B", ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1))),
    Piece("C", ((0, 0), (1, 0), (2, 0), (3, 0))),
    Piece("D", ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))),
    Piece("E", ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))),
    Piece("F", ((0, 0), (0, 1), (1, 0), (2, 0), (2, 1))),
    Piece("G", ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0))),
    Piece("H", ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2))),
    Piece("I", ((0, 0), (1, 0), (1, 1), (2, 1))),
    Piece("J", ((0, 0), (1, 0), (2, 0), (2, 1), (3, 1))),
)




def print_board(solution: dict[str, set[Coord]], hidden: set[Coord]) -> None:
    rendered: dict[Coord, str] = {}

    for r in range(8):
        for c in range(7):
            coord = (r, c)

            if coord in BLACK:
                rendered[coord] = "⬛"
            elif coord in hidden:
                rendered[coord] = "⬜"
            else:
                rendered[coord] = "⬛"

    for name in sorted(solution):
        for coord in solution[name]:
            rendered[coord] = name

    for r in range(8):
        print("".join(f"{rendered[(r, c)]}" for c in range(7)))




def placements_for_target(target: Coord, free: set[Coord], pieces: tuple[Piece, ...],) -> list[tuple[int, Piece, set[Coord]]]:
    options: list[tuple[int, Piece, set[Coord]]] = []

    for piece_index, piece in enumerate(pieces):
        for shape in VARIANTS[piece.name]:
            for sr, sc in shape:
                anchor_r = target[0] - sr
                anchor_c = target[1] - sc

                cells = {
                    (anchor_r + r, anchor_c + c)
                    for r, c in shape
                }

                if cells <= free:
                    options.append((piece_index, piece, cells))

    return options


def solve(free: set[Coord],    pieces: tuple[Piece, ...], placed: dict[str, set[Coord]] | None = None,) -> dict[str, set[Coord]] | None:
    if placed is None:
        placed = {}

    if not pieces:
        return placed if not free else None

    best_options: list[tuple[int, Piece, set[Coord]]] | None = None

    for target in sorted(free):
        options = placements_for_target(target, free, pieces)

        if not options:
            return None

        if best_options is None or len(options) < len(best_options):
            best_options = options

    if best_options is None:
        return None

    for piece_index, piece, cells in best_options:
        rest = pieces[:piece_index] + pieces[piece_index + 1:]

        new_placed = dict(placed)
        new_placed[piece.name] = cells

        result = solve(free=free - cells, pieces=rest, placed=new_placed,)

        if result is not None:
            return result

    return None




def build_hidden_cells(target_date: date) -> tuple[set[Coord], tuple[str, str, str]]:
    labels = (
        MONTHS[target_date.month],
        str(target_date.day),
        WEEKDAYS[target_date.weekday()],
    )

    label_to_coord = {
        label: coord
        for coord, label in BOARDLABELS.items()
    }

    try:
        hidden = {label_to_coord[label] for label in labels}
    except KeyError as e:
        raise RuntimeError(f"Метка не найдена на поле: {e}") from e

    return hidden, labels


def validate_board() -> None:
    black_with_labels = BLACK & set(BOARDLABELS)

    if black_with_labels:
        raise RuntimeError(f"Чёрные клетки не должны иметь меток: {sorted(black_with_labels)}")

    if len(set(BOARDLABELS.values())) != len(BOARDLABELS):
        raise RuntimeError("На поле есть повторяющиеся метки")

    piece_area = sum(len(piece.cells) for piece in PIECES)
    expected_area = len(PLAYABLELABELS) - 3

    if piece_area != expected_area:
        raise RuntimeError(f"Фигуры закрывают {piece_area} клеток, а нужно {expected_area}")




def shape_to_text(shape: Shape) -> str:
    max_r = max(r for r, _ in shape)
    max_c = max(c for _, c in shape)

    grid = []

    for r in range(max_r + 1):
        row = []
        for c in range(max_c + 1):
            if (r, c) in shape:
                row.append("██")
            else:
                row.append("  ")
        grid.append("".join(row))

    return "\n".join(grid)

def print_pieces() -> None:
    print("Фигуры:")
    print()

    for piece in PIECES:
        print(f"{piece.name}:")
        print(shape_to_text(piece.cells))
        print()




def build_variants() -> dict[str, tuple[Shape, ...]]:
    result: dict[str, tuple[Shape, ...]] = {}

    for piece in PIECES:
        result[piece.name] = variants(piece)

    return result




def normalize(cells: list[Coord]) -> Shape:
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)

    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def variants(piece: Piece) -> tuple[Shape, ...]:
    result: set[Shape] = set()

    for mirror in (False, True):
        for rotation in range(4):
            transformed: list[Coord] = []
            for r, c in piece.cells:
                x = r
                y = -c if mirror else c
                for _ in range(rotation):
                    x, y = y, -x
                transformed.append((x, y))
            result.add(normalize(transformed))

    return tuple(sorted(result))




def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as e:
        raise argparse.ArgumentTypeError("Дата должна быть существующей датой в формате YYYY-MM-DD") from e


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Решатель календарной головоломки",
    )
    parser.add_argument(
        "--date",
        type=parse_date,
        default=date.today(),
        help="Дата в формате YYYY-MM-DD. По умолчанию сегодня",
    )
    args = parser.parse_args()
    target_date: date = args.date
    print(f"Дата: {target_date.isoformat()}")
    global VARIANTS
    VARIANTS = build_variants()
    #print_pieces()
    validate_board()

    hidden, labels = build_hidden_cells(target_date)
    free = PLAYABLELABELS - hidden
    print(f"Открытые клетки: {labels[0]}, {labels[1]}, {labels[2]}")


    solution = solve(free, PIECES)
    if solution is None:
        print("Решение не найдено")
        return
    print_board(solution, hidden)


if __name__ == "__main__":
    main()