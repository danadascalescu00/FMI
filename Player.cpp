#include "Player.h"

Player::Player(const Position& pos, const char& sym, int l, const unsigned int& a) : Character(pos, sym, l, a)
{
    weapon = new Revolver();
    armor = new Armor();
}

Player::~Player()
{
    delete weapon;
    delete armor;
}



