#include "Armor.h"

Armor::Armor(double x, double y) : BonusHealth(x) , BonusDamageWeapon(y)
{
}

Armor::Armor(const Armor &armor)
{
    BonusHealth = armor.BonusHealth;
    BonusDamageWeapon = armor.BonusDamageWeapon;
}

Armor& Armor::operator=(const Armor& armor)
{
    if(this == &armor) return *this;

    BonusHealth = armor.BonusHealth;
    BonusDamageWeapon = armor.BonusDamageWeapon;

    return *this;
}

double Armor::GetBonusHealth() const
{
    return BonusHealth;
}

double Armor::GetBonusDamageWeapon() const
{
    return BonusDamageWeapon;
}

Armor::~Armor()
{
    BonusHealth = BonusDamageWeapon = 0.0;
}
