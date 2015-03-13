#include "queen.h"
#include<iostream>
using namespace std;

Queen::Queen()
{row = column = -1;}

int Queen::getRow() const
{return this->row;}

int Queen::getColumn() const
{return this->column;}


int Queen::setRow(const int x)
{return this->row = x;}

int Queen::setColumn(const int x)
{return this->column = x;}

int Queen::advanceCol()
{return this->column = ++(this->column);}
