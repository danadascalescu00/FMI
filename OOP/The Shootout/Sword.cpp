#include "Sword.h"

Sword::Sword(double D) : Weapon(2,D)
{
}

bool Sword::canRiseFromDead()
{
    return false;
}

bool Sword::canAttackTwice()
{
    return false;
}

void Sword::RiseFromDead()
{
    std::cout<<"The sword doesn't have this power";
}

Sword::~Sword()
{
}
