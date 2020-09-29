#include "Enemy.h"

Enemy::Enemy(const Position& pos, const char& sym, int life, const unsigned int& area) : Character(pos, sym, life, area)
{
    weapon = new Sword();
}

Enemy::~Enemy()
{
    delete weapon;
}

