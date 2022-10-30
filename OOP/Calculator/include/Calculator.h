#ifndef CALCULATOR_H
#define CALCULATOR_H

#include "Operand.h"
#include "Operation.h"
#include <cstdlib>
#include <chrono>
#include <thread>
#include <algorithm>

class Calculator
{
        Operand first_operand, second_operand, memory;
        Operation user_input;
        bool read;
        void DisplayLegend();
    public:
        Calculator();
        void operator()();
        ~Calculator();
};

#endif // CALCULATOR_H
