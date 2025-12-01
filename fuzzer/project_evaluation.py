import os

SEEDS = [
    """
#include <stdio.h>

int main() {
    int a = 5, b = 3;
    printf("sum=%d\\n", a + b);
    printf("product=%d\\n", a * b);
    return 0;
}
""",
    """#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        if (i % 2 == 0)
            printf("%d is even\\n", i);
        else
            printf("%d is odd\\n", i);
    }
    return 0;
}
""",
    """
#include <stdio.h>

int sum(int *a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}

int main() {
    int arr[5] = {1,2,3,4,5};
    printf("sum=%d\\n", sum(arr, 5));
    return 0;
}
""",
    """
#include <stdio.h>

struct Point {
    int x, y;
};

int main() {
    struct Point p = {3, 7};
    printf("(%d, %d)\\n", p.x, p.y);
    return 0;
}
""",
    """
#include <stdio.h>

typedef unsigned int uint;

int main() {
    uint x = 42;
    uint *p = &x;
    printf("%u\\n", *p);
    return 0;
}
""",
    """
#include <stdio.h>

int fact(int n) {
    if (n <= 1) return 1;
    return n * fact(n-1);
}

int main() {
    printf("%d\\n", fact(6));
    return 0;
}
""",
    """
#include <stdio.h>

int main() {
    char s[] = "hello";
    for (int i = 0; s[i]; i++)
        putchar(s[i]);
    putchar('\\n');
    return 0;
}
""",
    """
#include <stdio.h>

enum Color { RED, GREEN, BLUE };

int main() {
    enum Color c = GREEN;
    printf("color=%d\\n", c);
    return 0;
}
""",
    """
#include <stdio.h>

int main() {
    unsigned x = 0x5;   // 0101
    unsigned y = 0xA;   // 1010
    printf("%u\\n", x ^ y);
    return 0;
}
""",
    """
#include <stdio.h>

int inc(int x) { return x + 1; }

int apply(int (*f)(int), int v) {
    return f(v);
}

int main() {
    printf("%d\\n", apply(inc, 10));
    return 0;
}
""",
]


def get_seeds() -> list[str]:
    """
    For the evaluation without seeds, this returns an empty list,
    for the evaluation with seeds, this returns a list of high-quality seeds.

    Set the environment variable PROVIDE_SEEDS when running the Docker container to enable seeds.
    """
    if os.environ.get("PROVIDE_SEEDS", False):
        return SEEDS
    return []
