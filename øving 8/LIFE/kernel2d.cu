



__global__ void step(int *C, int *M) {
    int count;
    int n_x = blockDim.x * gridDim.x;
    int x = threadIdx.x + blockDim.x * blockIdx.x;
    int y = threadIdx.y + blockDim.y * blockIdx.y;
    int threadId = y * n_x + x;
    int x_left; int x_right; int y_down; int y_up;

    if(x == 0) {x_left= n_x - 1;} else {x_left = x - 1;}
    if(x == n_x - 1) {x_right = 0;} else {x_right= x + 1;}
    if(y == 0) {y_down = n_x - 1;} else {y_down = y - 1;}
    if(y == n_x - 1) {y_up = 0;} else {y_up = y + 1;}


    count = C[y*n_x+x_left] + C[y_down*n_x+x]
        + C[y*n_x+x_right] + C[y_up*n_x+x] + C[y_up*n_x+x_left]
        + C[y_down*n_x+x_right] + C[y_down*n_x+x_left]
        + C[y_up*n_x+x_right];

    if(count < 2 || count > 3) M[threadId] = 0; // cell dies
    if(count == 2) M[threadId] = C[threadId];// cell stays the same
    if(count == 3) M[threadId] = 1; // cell either stays alive, or is born
}