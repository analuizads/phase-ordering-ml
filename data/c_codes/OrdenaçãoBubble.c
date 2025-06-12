#include <stdio.h>

void bubbleSort(int v[], int n) {
    for (int i = 0; i < n-1; i++)
        for (int j = 0; j < n-i-1; j++)
            if (v[j] > v[j+1]) {
                int temp = v[j];
                v[j] = v[j+1];
                v[j+1] = temp;
            }
}

int main() {
    int v[] = {5, 3, 8, 4, 2};
    int n = 5;
    bubbleSort(v, n);
    for (int i = 0; i < n; i++)
        printf("%d ", v[i]);
    return 0;
}
