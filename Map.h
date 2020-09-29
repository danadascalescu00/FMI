#ifndef MAP_H
#define MAP_H

#include <vector>
#include<bits/stdc++.h>
#include <stdexcept>

#include "Utility.h"

class Map
{
    protected:
        unsigned int Height, Width;
        char **Land;
    //std::vector<std::vector<char> > Land;
    public:
        Map(const unsigned int& = 24, const unsigned int& = 24); //Constructor with parameters
        Map(const Map& ); //Copy constructor
        Map operator=(const Map& );  //Overload assigment operator
        const unsigned int GetHeight() const;
        const unsigned int GetWidth() const;
        bool isCharacter(const Position& ) const; //It returns true if an character is at the given position as parameter on the map
        void AddCell(const Position& , const char& ); //This method fills the map with a symbol(a character or a space ) at the given position
        friend std::ostream& operator<<(std::ostream& , const Map& ); //Overload the output operator for displaying the map
        ~Map(); //Destructor
};

#endif // MAP_H

