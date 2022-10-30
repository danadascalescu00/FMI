#include "Operation.h"

using namespace std;

Operation::Operation(string op) : operation(op)
{
    this->arity = validate(op);
}

short Operation::validate(string op) const
{
    string *p = (string *)find(arity1, arity1 + 7, op);
    if(p != arity1 + 7) return 1;

    string *p2 = (string *)find(arity2, arity2 + 5, op);
    if(p != arity2 + 5) return 2;

    throw invalid_argument("Invalid input!");
}

short Operation::GetArity() const
{
    return arity;
}

char Operation::GetSymbol() const
{
    return operation.back();
}

std::istream & operator>>(std::istream & in, Operation& op)
{
    in>>op.operation;
    op.arity = op.validate(op.operation);
    return in;
}

std::ostream & operator<<(std::ostream & out, const Operation& op)
{
    out<<op.operation;
    return out;
}
