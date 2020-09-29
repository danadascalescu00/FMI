#include "Utility.h"

ostream& operator<<(ostream& out, const Position& p)
{
    out << "(" << p.first << "," << p.second << ")" ;
    return out;
}
