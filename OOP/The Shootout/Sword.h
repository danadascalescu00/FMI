#ifndef SWORD_H
#define SWORD_H

#include "Weapon.h"
#include <iostream>


class Sword : public Weapon
{
    public:
        Sword(double = 45.0 );
        bool canRiseFromDead();
        bool canAttackTwice();
        void RiseFromDead();
        ~Sword();
};

#endif // SWORD_H
