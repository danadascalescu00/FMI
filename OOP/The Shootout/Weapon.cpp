#include "Weapon.h"

Weapon::Weapon(const unsigned int& R, double D) : Range(R) , Damage(D)
{
}

unsigned int Weapon::GetRange() const
{
    return Range;
}

double Weapon::GetDamage()
{
    return Damage;
}

void Weapon::SetDamage(double damage)
{
    Damage = damage;
}

Weapon::~Weapon()
{
    Range = 0;
    Damage = 0.0;
}

