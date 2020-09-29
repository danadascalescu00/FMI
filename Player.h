#ifndef PLAYER_H
#define PLAYER_H

#include "Character.h"
#include "Revolver.h"
#include "Armor.h"
#include <ostream>
#include <string>

class Player : public Character
{
    public:
        Player(const Position& = {2, 2} , const char& = 'P', int = 7, const unsigned int& = 10 );
        ~Player();
};

#endif // PLAYER_H
