#ifndef ENEMY_H
#define ENEMY_H

#include "Character.h"
#include "Sword.h"
#include "Armor.h"

class Enemy : public Character
{
    public:
        Enemy(const Position& , const char& ='E', int = 2, const unsigned int& = 5 );
        ~Enemy();
};

#endif // ENEMY_H
