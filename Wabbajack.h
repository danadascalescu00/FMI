#ifndef WABBAJACK_H
#define WABBAJACK_H

#include "Weapon.h"
#include <iostream>

class Wabbajack : public Weapon     ///This weapon can be used only by a wizard
{
    protected:
        bool Ressurection;  //Once per game the wizard can rise from dead
        bool BonusAtacks;   //A wizard can attack once or twice when his turn comes
    public:
        Wabbajack(const unsigned int& = 5 , double = 40.0);
        ~Wabbajack();
        bool canRiseFromDead();
        bool canAttackTwice();
        void RiseFromDead(); //Once the wizard used this power, he will not have the ability to attack twice
};

#endif // WABBAJACK_H
