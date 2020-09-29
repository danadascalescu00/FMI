#ifndef WEAPON_H
#define WEAPON_H


class Weapon
{
    protected:
        unsigned int Range;
        double Damage;
    public:
        Weapon(const unsigned int& = 10 , double = 20.0 );
        unsigned int GetRange() const;
        double GetDamage();
        void SetDamage(double );
        virtual bool canRiseFromDead() = 0;
        virtual bool canAttackTwice() = 0;
        virtual void RiseFromDead() = 0;
        virtual ~Weapon() = 0; //Pure virtual destructor
};

#endif // WEAPON_H
