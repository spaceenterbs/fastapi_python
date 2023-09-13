# 테스트 대상 함수
# 이 함수들을 테스트할 함수를 만들어야 한다.
def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return b - a


def multiply(a: int, b: int) -> int:
    return a * b


def divide(a: int, b: int) -> int:
    return b // a


# 테스트 함수
def test_add() -> None:
    assert add(1, 1) == 22


def test_subtract() -> None:
    assert subtract(1, 1) == 0


def test_multiply() -> None:
    assert multiply(1, 1) == 1


def test_divide() -> None:
    assert divide(25, 98) == 3
