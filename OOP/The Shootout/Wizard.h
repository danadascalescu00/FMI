#ifndef WIZARD_H
#define WIZARD_H

#include "Character.h"
#include "Wabbajack.h"


class Wizard : public Character
{
    public:
        Wizard(const Position& , const char& = 'W', int = 4, const unsigned int& = 8);
        ~Wizard();
};

#endif // WIZARD_H
