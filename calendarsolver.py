#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import argparse

Coord = tuple[int, int]

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


@dataclass(frozen=True)
class Piece:
    name: str
    cells: tuple[Coord, ...]


BLACK = {
    (0, 6), (1, 6),
    (7, 0), (7, 1), (7, 2), (7, 3),
}

BOARD_LABELS: dict[Coord, str] = {
    (0, 0): "ЯНВ", (0, 1): "ФЕВ", (0, 2): "МАР", (0, 3): "АПР", (0, 4): "МАЙ", (0, 5): "ИЮН",
    (1, 0): "ИЮЛ", (1, 1): "АВГ", (1, 2): "СЕН", (1, 3): "ОКТ", (1, 4): "НОЯ", (1, 5): "ДЕК",

    (2, 0): "1",  (2, 1): "2",  (2, 2): "3",  (2, 3): "4",  (2, 4): "5",  (2, 5): "6",  (2, 6): "7",
    (3, 0): "8",  (3, 1): "9",  (3, 2): "10", (3, 3): "11", (3, 4): "12", (3, 5): "13", (3, 6): "14",
    (4, 0): "15", (4, 1): "16", (4, 2): "17", (4, 3): "18", (4, 4): "19", (4, 5): "20", (4, 6): "21",
    (5, 0): "22", (5, 1): "23", (5, 2): "24", (5, 3): "25", (5, 4): "26", (5, 5): "27", (5, 6): "28",

    (6, 0): "29", (6, 1): "30", (6, 2): "31", (6, 3): "ПН", (6, 4): "ВТ", (6, 5): "СР", (6, 6): "ЧТ",
    (7, 4): "ПТ", (7, 5): "СБ", (7, 6): "ВС",
}

PLAYABLE = set(BOARD_LABELS)

PIECES = [
    Piece("A", ((0, 0), (1, 0), (2, 0), (2, 1))),
    Piece("B", ((0, 0), (1, 0), (2, 0), (2, 1))),
    Piece("C", ((0, 0), (1, 0), (2, 0), (3, 0))),
    Piece("D", ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))),
    Piece("E", ((0, 0), (0, 1), (0, 2), (1, 1), (2, 1))),
    Piece("F", ((0, 0), (0, 1), (1, 0), (2, 0), (2, 1))),
    Piece("G", ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0))),
    Piece("H", ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2))),
    Piece("I", ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2))),
    Piece("J", ((0, 0), (1, 0), (2, 0), (2, 1), (3, 1))),
]


def normalize(cells: list[Coord]) -> tuple[Coord, ...]:
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def variants(piece: Piece) -> list[tuple[Coord, ...]]:
    result = set()

    for mirror in (False, True):
        for rotation in range(4):
            cells = []

            for r, c in piece.cells:
                x, y = r, -c if mirror else c

                for _ in range(rotation):
                    x, y = y, -x

                cells.append((x, y))

            result.add(normalize(cells))

    return list(result)


VARIANTS = {piece.name: variants(piece) for piece in PIECES}


def solve(
    free: set[Coord],
    pieces: list[Piece],
    placed: dict[str, set[Coord]] | None = None,
) -> dict[str, set[Coord]] | None:
    if placed is None:
        placed = {}

    if not pieces:
        return placed if not free else None

    best_options = None

    for target in free:
        options = []

        for i, piece in enumerate(pieces):
            for shape in VARIANTS[piece.name]:
                for sr, sc in shape:
                    anchor_r = target[0] - sr
                    anchor_c = target[1] - sc

                    cells = {
                        (anchor_r + r, anchor_c + c)
                        for r, c in shape
                    }

                    if cells <= free:
                        options.append((i, piece, cells))

        if best_options is None or len(options) < len(best_options):
            best_options = options

        if best_options == []:
            return None

    assert best_options is not None

    for i, piece, cells in best_options:
        rest = pieces[:i] + pieces[i + 1:]
        result = solve(
            free - cells,
            rest,
            placed | {piece.name: cells},
        )

        if result:
            return result

    return None


def parse_date(value: str | None) -> date:
    if value is None:
        return date.today()

    return datetime.strptime(value, "%Y-%m-%d").date()


def print_board(solution: dict[str, set[Coord]], hidden: set[Coord]) -> None:
    rendered = {}

    for r in range(8):
        for c in range(7):
            coord = (r, c)

            if coord in BLACK:
                rendered[coord] = "██"
            elif coord in hidden:
                rendered[coord] = BOARD_LABELS[coord]
            else:
                rendered[coord] = "  "

    for name, cells in solution.items():
        for coord in cells:
            rendered[coord] = name

    for r in range(8):
        print(" ".join(f"{rendered[(r, c)]:>3}" for c in range(7)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        help="Дата в формате YYYY-MM-DD. По умолчанию сегодня.",
    )

    args = parser.parse_args()
    target_date = parse_date(args.date)

    labels = {
        MONTHS[target_date.month],
        str(target_date.day),
        WEEKDAYS[target_date.weekday()],
    }

    label_to_coord = {label: coord for coord, label in BOARD_LABELS.items()}
    hidden = {label_to_coord[label] for label in labels}

    free = PLAYABLE - hidden

    piece_area = sum(len(piece.cells) for piece in PIECES)

    if piece_area != len(free):
        print(f"Ошибка: фигуры закрывают {piece_area} клеток, а нужно {len(free)}")
        return

    print(f"Дата: {target_date.isoformat()}")
    print(f"Открытые клетки: {', '.join(sorted(labels))}")
    print()

    solution = solve(free, PIECES)

    if not solution:
        print("Решение не найдено")
        return

    print_board(solution, hidden)


if __name__ == "__main__":
    main()
