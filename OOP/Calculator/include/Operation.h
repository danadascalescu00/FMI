#ifndef OPERATION_H
#define OPERATION_H

#include <string>
#include <algorithm>
#include <stdexcept>

const std::string arity1[] = {"sqrt", "M+", "M-", "MC", "Clear", "MS", "q"};
const std::string arity2[] = {"+", "-", "*", "/", "^"};

class Operation
{
    std::string operation;
    short arity;
    short validate(std::string ) const;
    public:
        Operation(std::string = "MS");
        short GetArity() const;
        char GetSymbol() const;
        friend std::istream & operator>>(std::istream & , Operation &);
        friend std::ostream & operator<<(std::ostream & , const Operation &);
};

#endif // OPERATION_H
