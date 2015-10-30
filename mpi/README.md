This repository contains few codes which were given to us as assignments for our High Performance Computing course in the third semester of my Masters degree.
The codes were written using MPI

1. mat_vec.c : Matrix vector multiplication using 1d block partitioning 
               of the Input Matrix
               ( The matrix and vector are supplied as seperate files
                 via command line arguments. The code expects the files 
                 to be space seperated with a new line character
                 terminating each row of the matrix. The vector is 
                 required to be stored as a row vector following the same
                 convention as for the matrix. )

2. canon.c   : Matrix-Matrix Multiplication using Canon's Algorithm.
               ( The two matrices are supplied as seperate files via
                 command line arguments. The same file formatting
                 conventions are expected to be followed as in the mat_vec
                 code. Additionally,the algorithm requires the two matrices
                 to be square, of the same dimensions and the number of
                 processes to be  n^2 where n is the order of the square
                 matrices.)

3. parJacobi : Solution of a System of Linear Equations using Jacobi's 
               Method
               ( The system of linear equations Ax = b, along with the 
                 initial guess is supplied as a seperate file via command
                 arguments. The file is required to follow the same
                 conventions laid out above. The columns b and the initial
                 guess values are augumented to the coefficient matrix A.
                 Thus the input file is required to be specified as 
                 A|b|guess. )
