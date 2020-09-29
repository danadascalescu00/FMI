#include "Revolver.h"

Revolver::Revolver(const unsigned int& range, double damage) : Weapon(range, damage)
{
}

bool Revolver::canRiseFromDead()
{
    return false;
}

bool Revolver::canAttackTwice()
{
    return false;
}

void Revolver::RiseFromDead()
{
    std::cout<< "Revolver doesn't have this power.";
}

Revolver::~Revolver()
{
}
