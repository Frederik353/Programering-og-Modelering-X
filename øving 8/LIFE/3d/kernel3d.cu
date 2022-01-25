

__global__ void step(int *C, int *M, int *neighbours, int *Neigbor_count_gpu, int *ndim) {
    int count;
    int n_x = blockDim.x*gridDim.x; // total size
    //assumes equal length in all dimensions

    int coordinates[ndim] = [threadIdx.x + blockDim.x * blockIdx.x, threadIdx.y + blockDim.y * blockIdx.y, threadIdx.z + blockDim.z * blockIdx.z];
    // int x = threadIdx.x + blockDim.x * blockIdx.x; // coordinates
    // int y = threadIdx.y + blockDim.y * blockIdx.y;
    // int z = threadIdx.z + blockDim.z * blockIdx.z;

    int threadId = y * n_x + x;

    int x_down; int x_up; 
    int y_down; int y_up;
    int z_down; int z_up;

    //lower bound
    if(x == 0) {i_down = n_x - 1;} else {i_down = x - 1;}
    if(y == 0) {y_down = n_x - 1;} else {y_down = y - 1;}
    if(z == 0) {z_down = n_x - 1;} else {z_down = z - 1;}
    // upper bound
    if(x == n_x - 1) {i_up = 0;} else {i_up = x + 1;}
    if(y == n_x - 1) {y_up = 0;} else {y_up = y + 1;}
    if(z == n_x - 1) {z_up = 0;} else {z_up = z + 1;}

    int count = 0;
    int cell_neighbours[Neigbor_count_gpu][ndim];
    for (int i = 0; i < Neigbor_count_gpu; i++){
        for (int j = 0; j < ndim; j++){
            cell_neighbours[i * ndim + j] = neighbours[i * ndim + j] * coordinates[j]
        }
        count += C[]
    }

    // count = C[j*n_x+i_left] + C[j_down*n_x+i]
    //     + C[j*n_x+i_right] + C[j_up*n_x+i] + C[j_up*n_x+i_left]
    //     + C[j_down*n_x+i_right] + C[j_down*n_x+i_left]
    //     + C[j_up*n_x+i_right];

    // Modify matrix M according to the rules B3/S23:
    //A cell is "Born" if it has exactly 3 neighbours,
    //A cell "Survives" if it has 2 or 3 living neighbours; it dies otherwise.
    if(count < 2 || count > 3) M[threadId] = 0; // cell dies
    if(count == 2) M[threadId] = C[threadId];// cell stays the same
    if(count == 3) M[threadId] = 1; // cell either stays alive, or is born
}