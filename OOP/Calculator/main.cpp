#include "Calculator.h"

using namespace std;

void __attribute__((constructor)) Legend();

void Legend()
{
    std::cout<<std::endl<<'\t'<< "ADD -> + " <<std::endl;;
    std::cout<<'\t'<< "SUB -> - " <<std::endl;
    std::cout<<'\t'<< "Multiply -> * " <<std::endl;
    std::cout<<'\t'<< "Divide -> / " <<std::endl;
    std::cout<<'\t'<< "POW -> ^ " <<std::endl;
    std::cout<<'\t'<< "SQRT -> sqrt " <<std::endl;
    std::cout<<'\t'<< "MemSet -> MS " <<std::endl;
    std::cout<<'\t'<< "MemClear -> MC " <<std::endl;
    std::cout<<'\t'<< "MemPlus -> M+ " <<std::endl;
    std::cout<<'\t'<< "MemMinus -> M- " <<std::endl;
    std::cout<<'\t'<< "Clear -> C " <<std::endl;
    std::cout<<'\t'<< "Quit -> q " <<std::endl<<std::endl;
}

int main()
{
    Calculator calculator;
    calculator();
    return 0;
}
