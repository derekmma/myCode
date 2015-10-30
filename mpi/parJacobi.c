#include<stdio.h>
#include<mpi.h>
#include<stdlib.h>
#include<math.h>

#define epsilon 1E-5

double* jacobi(int it , int rank , int nrow , int col , int* row_count, double* initGuess , double* b, double A[][col] ) {

 int start , end , diag , i , j;
 double temp;
 start = 0;

 if ( rank == 0 ) {
  start = 0;
  end = row_count[ rank ] - 1 ; }
 else {
  for( i = rank - 1 ; i >= 0 ; i-- ) start += row_count[ i ];
  end = start + row_count[ rank ] - 1; }
 double* x = ( double* ) calloc( nrow , sizeof( double ) );


  for( i = 0, diag = start ; diag <= end ; diag++ , i++ ) {
  temp = 0;
  for( j = 0; j < col ; j++ ) {
   if ( j != diag ) temp += A[ i ][ j ] * initGuess[ j ]; 
  x[ i ] = ( b[ i ] - temp ) / A[ i ][ diag ]; } }
 return x; }

double norm(int n,double x[n]) {
 /*Returns two norm of the vector x*/
 float k=0.0;
 int i;
 for(i=0;i<n;i++) k += pow( (x[i]),2)  ;
 return sqrt(k); }

int main(int argc , char* argv[]) {

 int np , rank ;
 MPI_Init(NULL,NULL);
 MPI_Comm_size(MPI_COMM_WORLD,&np);
 MPI_Comm_rank(MPI_COMM_WORLD,&rank);

 int row, col, sq_flag, proc_flag,
     row_flag , convergence_flag, 
     *row_count, iteration, 
     *sendcounts, *displsA, *displsB;
 
 row_count = ( int* ) calloc( np , sizeof( int ) ); // required for 
 displsB = ( int* ) calloc( np , sizeof( int ) ) ;  // MPI_Allgatherv used later

 row = col = sq_flag = proc_flag = convergence_flag = row_flag = 0; 

 if ( rank == 0 ) {
  FILE *fp;
  char c;
  fp = fopen( argv[1], "r" ); /* compute matrix dimensions */
  while( ( c = fgetc( fp ) ) != EOF ) {
   if( c == ' ' && row == 0 ) col++;
   if( c == '\n' ) row++; }
   col++;
  fclose( fp );

  col -= 2;
  /* Square Matrix Check */
  if ( row != col ) {
   printf("\n==============ERROR===============\n");
   printf("Incompatible Input File.\nExiting\n");
   printf("====================================\n\n");
   sq_flag = 1; } 
  
  if ( np > row  ){
    printf("\n====================ERROR=======================\n");
    printf("Number of Processes greater than number of Rows.\nEXITING.\n");
    printf("================================================\n\n");
    proc_flag = 1; } }

 MPI_Bcast( &sq_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD );
 MPI_Bcast( &proc_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD);

 if ( ( sq_flag != 0 ) || ( proc_flag != 0 ) )  {
  MPI_Finalize();
  return 0 ; }  /* Exit if checks fail */

 MPI_Bcast( &row , 1 , MPI_INT , 0 , MPI_COMM_WORLD );
 MPI_Bcast( &col , 1 , MPI_INT , 0 , MPI_COMM_WORLD );

 double A[row][col] , B[row] ;
 double* init_guess = ( double * ) calloc( row , sizeof( double ) ) ;

 if (rank == 0 ) {
  int i , j ;
  FILE *fp;
  fp = fopen( argv[1] , "r" );
  while( !feof( fp ) ) {
   for (i = 0; i < row; i++) {
    for (j = 0; j < col; j++) fscanf( fp, "%lf" , &A[i][j] ); 
    fscanf( fp , "%lf" , &B[i] ); 
    fscanf( fp , "%lf" , &init_guess[i] ) ; } }
    
  /* Calculate number of rows each process is going to receive */
  int div = ( float ) row / np ;
  int rem = row % np ;
  for ( i = 0 ; i < np ; i++) *( row_count + i ) += div;
  for ( i = 0 ; i < rem ; i++) *( row_count + i ) += 1;
    
  sendcounts = ( int* ) calloc( np , sizeof( int ) );
  displsA = ( int* ) calloc( np , sizeof( int ) ) ;
    
  /* Calculate sendcounts and dispacement arrays needed for MPI_Scatterv */
  for ( i = 0 ; i < np ; i++ ) *( sendcounts + i ) = *( row_count + i ) * col ;
  for ( i = 1 ; i < np ; i++ ) {
   *( displsA + i ) = *( sendcounts + i - 1 ) + *( displsA + i - 1 ) ; 
   *( displsB + i ) = *( row_count + i - 1 ) + *( displsB + i - 1 ) ; } }
    
 MPI_Bcast( row_count , np , MPI_INT , 0 , MPI_COMM_WORLD );
 MPI_Bcast( displsB , np , MPI_INT , 0 , MPI_COMM_WORLD );
 
 double data[ row_count[ rank ] ][ col ],
        b[ row_count[ rank ] ];
 double *xNew , *recvbuf; 
 recvbuf = ( double* ) calloc( row , sizeof ( double ) );

 MPI_Scatterv( A , sendcounts , displsA , MPI_DOUBLE , &data , row_count[ rank ] * col , MPI_DOUBLE , 0 , MPI_COMM_WORLD);
 MPI_Scatterv( B , row_count , displsB , MPI_DOUBLE , &b , row_count[ rank ] , MPI_DOUBLE , 0 , MPI_COMM_WORLD );

 for( iteration = 1 ;  ; iteration++ ) {

  MPI_Bcast( init_guess , row , MPI_DOUBLE , 0 , MPI_COMM_WORLD );
  
  xNew = jacobi( iteration , rank , row_count[ rank ] , col , row_count , init_guess , b , data );
  MPI_Allgatherv( xNew , row_count[ rank ] , MPI_DOUBLE , recvbuf , row_count , displsB , MPI_DOUBLE , MPI_COMM_WORLD ); 
 
  free(xNew);
 
  if (rank == 0) {
   int i;
   
   if ( fabs( norm( row , init_guess ) - norm( row , recvbuf ) ) < epsilon )  {
    printf("\n############################ RESULT ###############################");
    printf("\n\nThe Eucledian Norm has dropped below the tolerance level of %1.0e.\nNumber of Iterations = %d\n",epsilon,iteration);
    for( i = 0 ; i < row ; i++) printf("x%d = %lf\n", i , recvbuf[ i ]);
    printf("\n###################################################################\n\n");
    convergence_flag = 1; }
   else {
    for ( i = 0 ; i < row ; i++ ) *( init_guess + i ) = *( recvbuf + i ); } } 
    
   MPI_Bcast(&convergence_flag , 1 , MPI_INT, 0 , MPI_COMM_WORLD);
   if ( convergence_flag == 1 ) break ; }

 if (rank == 0 ) { free(sendcounts); free(displsA);}
 free(init_guess); free(row_count) ;
 free(displsB); free(recvbuf);
 MPI_Finalize();
 return 0;
} 
