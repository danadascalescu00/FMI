#ifndef OPERAND_H
#define OPERAND_H

#include <iostream>
#include <stdexcept>
#include <cmath>

using namespace std;

class Operand
{
    float number;
    public:
        Operand(float = 0);
        void operator=(float );
        float operator+(const Operand& );
        float operator-(const Operand& );
        float operator*(const Operand& );
        float operator/(const Operand& );
        float operator^(const Operand& );
        float SquareRoot();
        friend istream & operator>>(istream& , Operand& );
        friend ostream & operator<<(ostream& , const Operand& );
};

#endif // OPERAND_H
