#include <stdio.h>

int potencia(int base, int exp) {
    if (exp == 0) return 1;
    return base * potencia(base, exp - 1);
}

int main() {
    int base = 2, exp = 5;
    printf("%d^%d = %d\n", base, exp, potencia(base, exp));
    return 0;
}
