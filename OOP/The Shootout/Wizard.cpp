#include "Wizard.h"

Wizard::Wizard(const Position& pos, const char& sym, int life, const unsigned int& area) : Character(pos, sym, life, area)
{
    weapon = new Wabbajack();
}

Wizard::~Wizard()
{
    delete weapon;
}


