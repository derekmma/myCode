#include "board.h" 

#define maxQueens 8

Board::Board()
{
 int i;
 this->queenNo = new Queen[maxQueens];
 this->basePtr = this->queenNo;
 for (i=0;i<maxQueens;i++,queenNo++)
 {
  (this->queenNo)->setRow(i);
  (this->queenNo)->setColumn(-1);
 }
 this->queenNo = this->basePtr;
 (this->queenNo)->setColumn(0);
 (this->queenNo)++;
}

Board::~Board(){}

Queen Board::placeQueen(Queen& q)
{
 if (q.getColumn() < 0){q.setColumn(0);}
 if (q.getColumn() > maxQueens - 1) {q.setColumn(-2);}
 return q;
}

bool Board::checkAttack(Queen* q,const int row,const int col)
// returns false if the queen q is under attack
{
 Queen* temp =q;
 int i;
 bool check=false;
 for(i=row;i>0;i--)
 {
  temp--;
  int pqRow = temp->getRow();
  int pqCol = temp->getColumn();
  check = (pqCol == col)||
          (pqCol == col - (row-pqRow))||
          (pqCol == col + (row-pqRow));
  if(check){return true;}
 }
 return check;
}

Queen* Board::checkBoard(Queen* q)
{
 int i;
 for (i=0;i<maxQueens;i++)
 {
  int row = q->getRow(); int col = q->getColumn();
  if(checkAttack(q,row,col)){q->advanceCol();}
  else{break;}
 }
  placeQueen(*q); // checks if Queen is to kept on the board or removed
  if( q->getColumn() < 0 ){q--;q->advanceCol();checkBoard(q);}
  if (q->getRow() == maxQueens-1){return q;}
  else{q++; placeQueen(*q);checkBoard(q);}
}

void Board::printBoard()
{
 placeQueen(*queenNo);
 checkBoard(queenNo);
 int i;
 cout<<"\nOne of the Final Configurations of the 8 Queens Problem is:\n";
 queenNo = basePtr;
 for(i=0;i<maxQueens;i++,queenNo++)
 {
  cout<<"Row = " << queenNo->getRow() <<" Col = "<<queenNo->getColumn()<<endl;
 }
}
