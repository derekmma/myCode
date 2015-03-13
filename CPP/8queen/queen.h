#ifndef __queen_h_

#define __queen_h_
class Queen
{
  
private:
    int row, column;

public:
  Queen();
  int getRow() const;
  int getColumn()const;
  int setRow(const int);
  int setColumn(const int);
  int advanceCol();
};

#endif
