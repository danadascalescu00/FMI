#ifndef MAPMANAGEMENT_H
#define MAPMANAGEMENT_H

#include "Utility.h"

class MapManagement
{
    protected:
        Position position;
        char Persona; //Symbol of the character which will appear on the map
        void SetPosition(const Position& ); //This function will set a new position
    public:
        MapManagement(const Position& = {1 , 1}, const char& = ' ');
        Position GetPosition() const; //Get position of the character
        char GetCharacter() const;

};

#endif // MAPMANAGEMENT_H
