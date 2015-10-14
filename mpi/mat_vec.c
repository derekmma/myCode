#include<stdio.h>
#include<mpi.h>
#include<stdlib.h>

int main( int argc , char* argv[] ) {
 int np,rank;
 MPI_Init(NULL,NULL);
 MPI_Comm_rank(MPI_COMM_WORLD,&rank);
 MPI_Comm_size(MPI_COMM_WORLD,&np);

 int i , j ;
 int *row_count , *sendcounts , *displs;
 int row , col , vec_size , size_flag , proc_flag;
 row = col = vec_size = size_flag = proc_flag = 0;

 /* Read dimensions of input matrix and vector */
 if(rank == 0) {
  FILE *fp;
  char c;
  fp = fopen( argv[1], "r" ); /* compute matrix dimensions */
  while( ( c = fgetc( fp ) ) != EOF ) {
   if( c == ' ' && row == 0 ) col++;
   if( c == '\n' ) row++; }
  col++;
  fclose( fp );

  fp = fopen( argv[2] , "r" ); /* compute vector dimensions */
  while( ( c = fgetc( fp ) ) != EOF) if (c == ' ') vec_size++ ;
  vec_size++;
  fclose( fp );
 
  /* check to ensure dimensions are compatible */
  if (col != vec_size) { 
    printf("\n===========ERROR===========\n");
    printf("INCORRECT DIMENSIONS.\nEXITING.\n");
    printf("===========================\n\n");
    size_flag = 1;} 

  /* check to ensure that no of processes is 
     lesser than number of rows */
  if ( np > row  ){
    printf("\n====================ERROR=======================\n");
    printf("Number of Processes greater than number of Rows.\nEXITING.\n");
    printf("================================================\n\n");
    proc_flag = 1; }}
 
 MPI_Bcast( &size_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD); 
 MPI_Bcast( &proc_flag , 1 , MPI_INT , 0 , MPI_COMM_WORLD);

 if ( (size_flag != 0) || (proc_flag != 0) ) {
 MPI_Finalize();
 return 0 ; } /* Exit if checks fail */

 MPI_Bcast( &row , 1 , MPI_INT , 0 , MPI_COMM_WORLD );
 MPI_Bcast( &col , 1 , MPI_INT , 0 , MPI_COMM_WORLD ); 
 MPI_Bcast( &vec_size , 1 , MPI_INT , 0 , MPI_COMM_WORLD );

 double A[row][col];
 double x[vec_size];
 double y[row];
 
 if (rank == 0 ) {
  FILE *fp;
  fp = fopen(argv[1] , "r" );   /* Read input matrix */
  while( !feof( fp ) ) {
   for (i = 0; i< row; i++) {
    for (j = 0; j < col; j++)
     fscanf( fp, "%lf", &A[i][j]); } }
  fclose( fp );
  fp = fopen( argv[2] , "r" );   /* Read input vector */
  while( !feof( fp ) ){
   for (i = 0 ; i < vec_size ; i++)
     fscanf( fp , "%lf" , &x[i] ) ; }
  fclose(fp);

  /* Calculate number of rows each process is going to receive */
  row_count = (int*) calloc( np , sizeof( int ) );
  int div = ( float ) row / np ;
  int rem = row % np ;
  for ( i = 0 ; i < np ; i++) *( row_count + i ) += div;
  for ( i = 0 ; i < rem ; i++) *( row_count + i ) += 1;

  sendcounts = ( int* ) calloc( np , sizeof( int ) );
  displs = (int*) calloc( np , sizeof( int ) );
  
  /* Calculate sendcounts and dispacement arrays needed for MPI_Scatterv */
  for ( i = 0 ; i < np ; i++ ) *( sendcounts + i ) = *( row_count + i ) * col ;
  for ( i = 1 ; i < np ; i++ ) *( displs + i ) = *( sendcounts + i - 1) + *( displs + i - 1 )  ; }
 int proc_row;  
 MPI_Scatter( row_count , 1 , MPI_INT , &proc_row , 1 , MPI_INT , 0 , MPI_COMM_WORLD );
 double data[ proc_row ][ col ];
 double procMul[proc_row];

 MPI_Scatterv( A , sendcounts , displs , MPI_DOUBLE , &data , proc_row * col , MPI_DOUBLE , 0 , MPI_COMM_WORLD);
 MPI_Bcast( x , vec_size , MPI_DOUBLE , 0 , MPI_COMM_WORLD );

 /* Recalculate sendcounts (recvcounts) and displs for MPI_Gatherv */
 if ( rank == 0 ) 
  for ( i = 1 ; i < np ; i++ ) *( displs + i ) = *( row_count + i - 1) + *( displs + i - 1 )  ; 


 /* Perform Matrix Vector Multiplication */
 for( i = 0 ; i < proc_row ; i++ ) {
  procMul[i] = 0;
  for ( j = 0; j < col ; j++ )
   procMul[i] += data[i][j]*x[j]; } 
 
 MPI_Gatherv( procMul , proc_row , MPI_DOUBLE , y , row_count , displs , MPI_DOUBLE, 0 , MPI_COMM_WORLD  );

 if (rank == 0) {
  printf("\nA(%dx%d) x(%dx1) = \n",row,vec_size,vec_size);
  for(i=0;i<row;i++) printf("%lf ",y[i]);
  printf("\n\n"); }
  
 if (rank == 0 ) { free(row_count); free(sendcounts); free(displs); }
 MPI_Finalize();
 return 0;
}
