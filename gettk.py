def _TKK():
    return [406604, 1836941114]


def _RL(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        if d >= 'a':
            d = ord(d) - 87
        else:
            d = int(d)
        if b[c + 1] == '+':
            d = a >> d
        else:
            d = a << d
        if b[c] == '+':
            a = a + d & (pow(2, 32) - 1)
        else:
            a = a ^ d
    return a


def _TL(a: str):
    tkk = _TKK()
    b = tkk[0]
    d = [i for i in a.encode('utf8')]
    a = b
    for e in range(0, len(d)):
        a += d[e]
        a = _RL(a, "+-a^+6")
    a = _RL(a, "+-3^+b+-f")
    a = a ^ tkk[1]
    if a < 0:
        a = (a & (pow(2, 31) - 1)) + pow(2, 31)
    a %= pow(10, 6)
    return "%d.%d" % (a, a ^ b)


def get_tk(word):
    return _TL(word)


if __name__ == '__main__':
    print(get_tk('hello'))
