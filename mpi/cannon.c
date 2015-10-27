#include <mpi.h>
#include <stdio.h>

int main(int argc , char* argv[] ) {

 int np, rank;

 MPI_Init(NULL,NULL);
 MPI_Comm_rank( MPI_COMM_WORLD , &rank);
 MPI_Comm_size( MPI_COMM_WORLD , &np);

 int row , col , row1 , col1 , size_flag, sq_flag , proc_flag;
 row = col = row1 = col1 = size_flag = sq_flag = proc_flag = 0;

 if (rank == 0 ) {
  FILE *fp;
  char c;
  fp = fopen( argv[1], "r" ); /* compute matrix1 dimensions */
  while( ( c = fgetc( fp ) ) != EOF ) {
   if( c == ' ' && row == 0 ) col++;
   if( c == '\n' ) row++; }
  col++;
  fclose( fp );
  fp = fopen( argv[2], "r" ); /* compute matrix2 dimensions */
  while( ( c = fgetc( fp ) ) != EOF ) {
   if( c == ' ' && row1 == 0 ) col1++;
   if( c == '\n' ) row1++; }
  col1++;
  fclose( fp );

  /* Square Matrix Check */
  if ( ( row != col ) || (row1 != col1) ){
   printf("\n================ERROR================\n");
   printf("Input Matrices are not Square.\nExiting\n");
   printf("=======================================\n\n");
   sq_flag = 1; }

  /* Dimension Check */
  if ( row != row1 ) {
   printf("\n================ERROR=================\n");
   printf("Matrices are not of the same dimensions.\nExiting\n");
   printf("========================================\n\n");
   size_flag = 1; }

  /* Number of Processes Check */
  if (np != row *col){
   printf("\n==================ERROR=================\n");
   printf("Number of processes should be %d.\nExiting\n",row*col);
   printf("==========================================\n\n");
   proc_flag = 1; } }
 
 MPI_Bcast( &size_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD);
 MPI_Bcast( &sq_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD);
 MPI_Bcast( &proc_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD);

 if ( (sq_flag != 0) || (proc_flag != 0) || ( size_flag != 0  ) ) {
  MPI_Finalize();
  return 0 ; } /* Exit if checks fail */

 double A[row][col] , 
        B[row][col] , 
        C[row][col] ;

 if (rank == 0 ) {
  int i,j;
  FILE *fp;
  fp = fopen(argv[1] , "r" );   /* Read input matrix1 */
  while( !feof( fp ) ) {
   for (i = 0; i < row; i++) {
    for (j = 0; j < col; j++)
     fscanf( fp, "%lf", &A[i][j]); } }
  fclose( fp );
  fp = fopen(argv[2] , "r" );   /* Read input matrix2 */
  while( !feof( fp ) ) {
   for (i = 0; i < row; i++) {
    for (j = 0; j < col; j++)
     fscanf( fp, "%lf", &B[i][j]); } }
  fclose(fp); }


 double a,b;

 MPI_Scatter( A , 1 , MPI_DOUBLE , &a , 1 , MPI_DOUBLE , 0 , MPI_COMM_WORLD);
 MPI_Scatter( B , 1 , MPI_DOUBLE , &b , 1 , MPI_DOUBLE , 0 , MPI_COMM_WORLD);
 
 MPI_Bcast( &row , 1 , MPI_INT , 0 , MPI_COMM_WORLD );

 /* initializing virtual topology */
 MPI_Comm cartcomm;  /* Create New communicator */
 int dims[2] = {row,row} , 
     periods[2] = {1,1}  ,
     coords[2];
 
 MPI_Cart_create( MPI_COMM_WORLD , 2 , dims , periods , 1 , &cartcomm );
 MPI_Cart_coords(cartcomm , rank , 2 , coords);

 /* Transfer data among procs to get Initial Cannon Configuration */

 int sourceX , destX , 
     sourceY , destY , 
     i , j ;
 double temp , procMul = 0;

 MPI_Cart_shift( cartcomm , 1 , (int) rank / row , &sourceX , &destX);
 MPI_Cart_shift( cartcomm , 0 , rank % row , &sourceY , &destY);

 if ( rank >= row ) {
 MPI_Send( &a , 1, MPI_DOUBLE , sourceX , 1 , MPI_COMM_WORLD );
 MPI_Recv( &temp , 1, MPI_DOUBLE , destX , 1, MPI_COMM_WORLD , MPI_STATUS_IGNORE);
 a = temp ; }

 if (rank%row != 0){
 MPI_Send( &b , 1, MPI_DOUBLE , sourceY , 1 , MPI_COMM_WORLD );
 MPI_Recv( &temp , 1, MPI_DOUBLE , destY , 1, MPI_COMM_WORLD , MPI_STATUS_IGNORE);
 b = temp; }

 /* Begin Canon's Algorithm */

 procMul += a * b;
 for( i = 1 ; i < row ; i++ ) {
  MPI_Cart_shift( cartcomm , 1 , 1 , &sourceX , &destX);
  MPI_Cart_shift( cartcomm , 0 , 1 , &sourceY , &destY);
  MPI_Send( &a , 1, MPI_DOUBLE , sourceX , 1 , MPI_COMM_WORLD );
  MPI_Recv( &temp , 1, MPI_DOUBLE , destX , 1, MPI_COMM_WORLD , MPI_STATUS_IGNORE);
  a = temp ;
  MPI_Send( &b , 1, MPI_DOUBLE , sourceY , 1 , MPI_COMM_WORLD );
  MPI_Recv( &temp , 1, MPI_DOUBLE , destY , 1, MPI_COMM_WORLD , MPI_STATUS_IGNORE);
  b = temp;
  procMul += a * b; }

 if ( rank != 0 ) { 
  MPI_Send( &coords[0] , 1 , MPI_INT , 0 , 2 , MPI_COMM_WORLD );
  MPI_Send( &coords[1] , 1 , MPI_INT , 0 , 3 , MPI_COMM_WORLD ); 
  MPI_Send( &procMul , 1 , MPI_DOUBLE , 0 , 1 , MPI_COMM_WORLD ); }
 else {
  C[0][0] = procMul;
  int k ;
  for( k = 1 ; k < np ; k++){
   MPI_Recv( &i , 1 , MPI_INT , k , 2 , MPI_COMM_WORLD , MPI_STATUS_IGNORE );
   MPI_Recv( &j , 1 , MPI_INT , k , 3 , MPI_COMM_WORLD , MPI_STATUS_IGNORE );
   MPI_Recv( &C[i][j] , 1 , MPI_DOUBLE , k , 1 , MPI_COMM_WORLD , MPI_STATUS_IGNORE ); } 
 
 printf("\n");
 printf("Matrix A is :\n");
 for( i = 0 ; i < row ; i++){
  for( j = 0 ; j < row ; j++) printf("%.3lf\t",A[i][j]);
  printf("\n"); }
 printf("\n");

 printf("Matrix B is :\n");
 for( i = 0 ; i < row ; i++){
  for( j = 0 ; j < row ; j++) printf("%.3lf\t",B[i][j]);
  printf("\n"); }
 printf("\n");

 printf("Matrix C is A * B:\n");
 for( i = 0 ; i < row ; i++){
  for( j = 0 ; j < row ; j++) printf("%.3lf\t",C[i][j]); 
  printf("\n");} 
 printf("\n"); }

 MPI_Finalize();
 return 0; }
