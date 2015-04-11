#ifndef __board_h

#define __board_h

#include "queen.h"
#include <iostream>
using namespace std;
class Board
{
 private:
    Queen *queenNo;
 public: 
    Board();
    ~Board();
    Queen placeQueen(Queen&);
    bool checkAttack(Queen*, const int, const int);
    Queen* checkBoard(Queen*);
    void printBoard();
};

#endif
