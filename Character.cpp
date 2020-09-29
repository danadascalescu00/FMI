#include "Character.h"

Character::Character(const Position& pos, const char& sym, int life, const unsigned int& area) : MapManagement(pos, sym), Health(100.0) , Life(life), Area(area)
{
}

Character::~Character()
{
    Health = 0.0;
    Life = 0;
    Area = 0;
}

int Character::GetLife()
{
    return Life;
}

double Character::GetHealth()
{
    return Health;
}

bool Character::isDead() const
{
    return Life == 0;
}

unsigned int Character::GetArea() const
{
    return Area;
}

void Character::SetArea(unsigned int area)
{
    Area = area;
}

void Character::SetLife(int life)
{
    Life = life;
}

void Character::SetHealth(double health)
{
    Health = health;
}

void Character::Move(const Position& new_position)
{
    SetPosition(new_position);
}

bool Character::canMove(const Map& land, const Position& pos, const unsigned int& a)
{
    bool okay = true;
    Position verif(pos.first, pos.second + 1);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first, pos.second - 1);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first + 1, pos.second);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first - 1, pos.second);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first + 1, pos.second + 1);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first - 1, pos.second - 1);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first + 1, pos.second - 1);
    if(land.isCharacter(verif)) okay = false;

    verif = Position(pos.first - 1, pos.second + 1);
    if(land.isCharacter(verif)) okay = false;

    for(unsigned int i = 2; i <= a; i++)
    {
        verif = Position(pos.first, pos.second + i);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first, pos.second - i);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first + i, pos.second);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first - i, pos.second);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first + i, pos.second + i);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first - i, pos.second - i);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first + i, pos.second - i);
        if(land.isCharacter(verif)) okay = false;

        verif = Position(pos.first - i, pos.second + i);
        if(land.isCharacter(verif)) okay = false;
    }

    if(okay == true) return true;
        else return false;
}

Position Character::FindOut(const Map& land, const Position& pos, const unsigned int& a)
{
    Position verif(pos.first, pos.second + 1);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first, pos.second - 1);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first + 1, pos.second);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first - 1, pos.second);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first + 1, pos.second + 1);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first - 1, pos.second - 1);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first + 1, pos.second - 1);
    if(land.isCharacter(verif)) return verif;

    verif = Position(pos.first - 1, pos.second + 1);
    if(land.isCharacter(verif)) return verif;


    for(unsigned int i = 2; i <= a; i++)
    {
        verif = Position(pos.first, pos.second + i);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first, pos.second - i);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first + i, pos.second);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first - i, pos.second);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first + i, pos.second + i);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first - i, pos.second - i);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first + i, pos.second - i);
        if(land.isCharacter(verif)) return verif;

        verif = Position(pos.first - i, pos.second + i);
        if(land.isCharacter(verif)) return verif;
    }
}

Position Character::NextMove(const Map& land, const Position& pos, const unsigned int& area)
{
    Position new_position(pos.first, pos.second);
    Position return_position(pos.first, pos.second);
    unsigned int battlefield_height = land.GetHeight();
    unsigned int battlefield_width = land.GetWidth();

    for(unsigned int i = area; i >= 1; i--)
    {
        unsigned int j = rand() % 8;
        switch(j)
        {
            case 0 :{
                        new_position = Position(pos.first, pos.second + i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 1 :{
                        new_position = Position(pos.first + i, pos.second);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 2 :{
                        new_position = Position(pos.first - i, pos.second);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 3 :{
                        new_position = Position(pos.first, pos.second - i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 4 :{
                        new_position = Position(pos.first + i, pos.second + i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 5 :{
                        new_position = Position(pos.first - i, pos.second - i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 6 :{
                        new_position = Position(pos.first + i, pos.second - i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
            }
            case 7:{
                        new_position = Position(pos.first - i, pos.second + i);
                        if(!land.isCharacter(new_position))
                            if(new_position.first < battlefield_height && new_position.second < battlefield_width)
                                return new_position;
                        break;
                    }
        }
    }

    return return_position;
}
