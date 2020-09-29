#ifndef CHARACTER_H
#define CHARACTER_H

#include <string>
#include "Utility.h"
#include "Map.h"
#include "MapManagement.h"
#include "Weapon.h"
#include "Armor.h"

using namespace std;

class Character : public MapManagement
{
    protected:
        double Health;
        int Life;
        unsigned int Area;
    public:
        Weapon *weapon;
        Armor *armor;
        Character(const Position& = {0, 0}, const char& = 'c' , int = 3, const unsigned int& = 4);   //By default every character has 3 lives
        virtual ~Character() = 0; //Pure virtual destructor
        int GetLife();
        double GetHealth();
        bool isDead() const;
        unsigned int GetArea() const;
        void SetArea(unsigned int );
        void SetLife(int );
        void SetHealth(double );
        void Move(const Position& );
        bool canMove(const Map& , const Position& , const unsigned int& );  //The character can move only if within its area is not another character otherwise he will have to attack
        Position FindOut(const Map&, const Position&, const unsigned int& ); //Find out the position of the character which must be attack
        Position NextMove(const Map&, const Position&, const unsigned int& ); //The character will change his position
};

#endif // CHARACTER_H
