#include "Operand.h"

using namespace std;

Operand::Operand(float num) : number(num)
{
}

void Operand::operator=(float n)
{
    this->number = n;
}

float Operand::operator+(const Operand& op)
{
    float temp = number + op.number;
    return temp;
}

float Operand::operator-(const Operand& op)
{
    float temp = number - op.number;
    return temp;
}

float Operand::operator*(const Operand& op)
{
    float temp = number * op.number;
    return temp;
}

float Operand::operator/(const Operand& op)
{
    float temp = number / op.number;
    return temp;
}

float Operand::operator^(const Operand& op)
{
    float temp = pow(number, op.number);
    return temp;
}

float Operand::SquareRoot()
{
    float temp = number;
    temp = sqrt(temp);
    return temp;
}

istream & operator>>(istream& in, Operand& op)
{
    in>>op.number;
    return in;
}

ostream & operator<<(ostream& out, const Operand& op)
{
    out<<op.number;
    return out;
}
