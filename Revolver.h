#ifndef REVOLVER_H
#define REVOLVER_H

#include "Weapon.h"
#include <iostream>

class Revolver : public Weapon
{
    public:
        Revolver(const unsigned int& = 10 , double = 35.0);
        bool canRiseFromDead();
        bool canAttackTwice();
        void RiseFromDead();
        ~Revolver();
};

#endif // REVOLVER_H
