#include <stdio.h>       // printf
#include <bits/stdc++.h> // pow

const int ndim = 3;
const int str[] = {-1, 0, 1};
const int n = 3;
const int adjecent = pow(n, ndim);
const int p[ndim] = {0, 0, 0};

void print_str(int neighbors[adjecent][ndim], int prefix[ndim - 1], const int lenght)
{

    if (lenght == 1)
    {

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < ndim - 1; j++)
            {
                int index = 0;
                for (int k = 0; k < ndim - 1; k++)
                {
                    index += (prefix[k] + 1) * pow(ndim, ndim - (k + 1));
                }
                index += i;
                // printf("%i", index);
                // printf("%s", " ");
                // neighbors[foo + (n * (prefix[1] + 1)) + i][i] = prefix[i];
                neighbors[index][j] = prefix[j];
            }
            // printf("%s \n", "");
            // printf("%s \n", "---------------");
        }

        for (int i = 0; i < n; i++)
        {
            int index = 0;
            for (int k = 0; k < ndim - 1; k++)
            {
                index += (prefix[k] + 1) * pow(ndim, ndim - (k + 1));
            }
            index += i;

            // printf("%i \n", index);
            neighbors[index][ndim - 1] = str[i];
        }
        // printf("%s \n", " ");
    }
    else
    {
        for (int i = 0; i < n; i++)
        {
            prefix[ndim - lenght] = str[i];

            print_str(neighbors, prefix, lenght - 1);
        }
    }
}

int main()
{
    int neighbors[adjecent][ndim];
    int prefix[ndim - 1];

    print_str(neighbors, prefix, ndim);

    // for (int i = 0; i < pow(n, ndim); i++)
    // {
    //     for (int j = 0; j < ndim; j++)
    //     {
    //         neighbors[i][j] += p[j];
    //     }
    // }

    for (int i = 0; i < pow(n, ndim); i++)
    {
        for (int j = 0; j < ndim; j++)
        {
            printf("%i", neighbors[i][j]);
            printf("%s", " ");
        }
        printf("%s \n", "");
    }
}
