#ifndef ARMOR_H
#define ARMOR_H


class Armor
{
    protected:
        double BonusHealth;
        double BonusDamageWeapon;
    public:
        Armor(double = 10.0, double = 20.0 );
        Armor(const Armor& );
        Armor& operator=(const Armor& );
        double GetBonusHealth() const;
        double GetBonusDamageWeapon() const;
        ~Armor();
};

#endif // ARMOR_H
