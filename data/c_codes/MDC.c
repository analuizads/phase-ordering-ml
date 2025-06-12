#include <stdio.h>

int mdc(int a, int b) {
    if (b == 0) return a;
    return mdc(b, a % b);
}

int main() {
    int a = 48, b = 18;
    printf("MDC(%d, %d) = %d\n", a, b, mdc(a, b));
    return 0;
}
