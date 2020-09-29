#include "Wabbajack.h"

Wabbajack::Wabbajack(const unsigned int& range, double damage) : Weapon(range, damage)
{
    BonusAtacks = true;
    Ressurection = true;
}

Wabbajack::~Wabbajack()
{
    BonusAtacks = false;
    Ressurection = false;
}

bool Wabbajack::canRiseFromDead()
{
    if(Ressurection) return true;
        else return false;
}

bool Wabbajack::canAttackTwice()
{
    if(BonusAtacks) return true;
        else return false;
}

void Wabbajack::RiseFromDead()
{
    if(Ressurection == true)
    {
        Ressurection = false;
        BonusAtacks = false;
    }
}
