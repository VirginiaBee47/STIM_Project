


def test_func(p1, p2):
    p2.append(str(p1 ** 2))


if __name__ == "__main__":
    x = []
    test_func(2, x)
    print(x)