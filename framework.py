from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Partition:
    """Element of the partition algebra"""

    size: int
    """Size of first line of the element"""

    repr: tuple[int]
    """Standart representation we've choosen for partition"""

    components: int
    """Count of components in partition (used for generation of elements)"""

    @lru_cache
    def __add__(self, y):
        """Intersection of partitions"""

        if self.size != y.size:
            raise ArithmeticError

        # That's an operation of normalizing pairs, in nutshell.

        labels: dict[(int, int), int] = {}
        next_free_label = 0

        new_repr = ()

        for pair in zip(self.repr, y.repr):
            if pair not in labels:
                labels[pair] = next_free_label
                next_free_label += 1

            new_repr += (labels[pair],)

        return Partition(self.size, new_repr, next_free_label - 1)

    @lru_cache
    def __mul__(self, y):
        if self.size != y.size:
            raise ArithmeticError

        size = self.size
        y = Partition(size, tuple(i + 2 * size for i in y.repr), y.components)

        labels = list(range(4 * size))
        next_in_class = list(range(4 * size))

        for class1, class2 in zip(self.repr[size:], y.repr[:size]):
            if labels[class1] != labels[class2]:
                next_in_class[class1], next_in_class[class2] = (
                    next_in_class[class2],
                    next_in_class[class1],
                )

                current = next_in_class[class1]
                while current != class1:
                    labels[current] = labels[class1]
                    current = next_in_class[current]

        # Normalizing build label system.

        new_labels = [-1 for _ in range(4 * size)]
        next_free_label = 0
        new_partition = ()

        for class_ in self.repr[:size] + y.repr[size:]:
            label = labels[class_]

            if new_labels[label] == -1:
                new_labels[label] = next_free_label
                next_free_label += 1

            new_partition += (new_labels[label],)

        return Partition(size, new_partition, next_free_label - 1)


@lru_cache
def generate_partitions_given_size(size: int) -> list[Partition]:
    """Generates all possible partitions of given size"""

    repr_size = size * 2
    partitions = [Partition(size, (), 0)]

    for new_size in range(repr_size):
        new_partitions = []

        for partition in partitions:
            for new_component in range(partition.components):
                new_partition = Partition(
                    size, partition.repr + (new_component,), partition.components
                )

                new_partitions.append(new_partition)

            new_partition = Partition(
                size,
                partition.repr + (partition.components,),
                partition.components + 1,
            )

            new_partitions.append(new_partition)

        partitions = new_partitions

    return partitions


if __name__ == "__main__":
    part_ = generate_partitions_given_size(2)

    for a in part_:
        for b in part_:
            print(a, b, a * b)
