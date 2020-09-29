#include "MapManagement.h"

void MapManagement::SetPosition(const Position& NewPosition)
{
    position = NewPosition;
}

MapManagement::MapManagement(const Position& pos, const char& sym) : position(pos) , Persona(sym)
{
}

Position MapManagement::GetPosition() const
{
    return position;
}

char MapManagement::GetCharacter() const
{
    return Persona;
}
