from enum import StrEnum, auto


class RouteTags(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return " ".join([w.title() for w in name.split("_")])

    FILMS = auto()
    FILMS_COLLECTIONS = auto()

    V1 = auto()
