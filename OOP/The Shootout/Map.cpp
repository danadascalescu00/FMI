#include "Map.h"

Map::Map(const unsigned int& height, const unsigned int& width) : Height(height) , Width(width)
{
    Land = new char*[Height];
    for(unsigned int i = 0; i < Height; i++)
    {
        Land[i] = new char[Width];
        std::fill(Land[i], Land[i] + Width, ' ');
    }
    //Land.resize(width);
    //for_each(Land.begin(), Land.end(), [](std::vector<char>& v){v.resize(height)});
}

Map::Map(const Map& land) : Map(land.Height, land.Width)
{
    for(unsigned int i = 0; i < Height; i++)
        std::copy(land.Land[i], land.Land[i] + Width, Land[i]);
}

Map Map::operator=(const Map& land)
{
    if(this != &land)
    {
        for(unsigned int i = 0; i < Height; i++)
            delete[] Land[i];
        delete[] Land;

        Height = land.Height;
        Width = land.Width;

        Land = new char *[Height];
        for(unsigned int i = 0; i < Height; i++)
        {

            Land[i] = new char[Width];
            std::copy(land.Land[i], land.Land[i] + Width, Land[i]);
        }
    }
    return *this;
}

const unsigned int Map::GetHeight() const
{
    return Height;
}

const unsigned int Map::GetWidth() const
{
    return Width;
}

bool Map::isCharacter(const Position& position) const
{
    if(position.first < Height && position.second < Width)
        if(Land[position.first][position.second] != ' ') return true;
    return false;
}

void Map::AddCell(const Position& position, const char& persona)
{
    if(position.first >= Height || position.second >= Width)
        throw std::out_of_range("Out of map!");
    Land[position.first][position.second] = persona;
}

std::ostream& operator<<(std::ostream& out, const Map& land)
{
    for(unsigned int i = 0; i < land.Width + 2; i++)
        out << '-';
    out << std::endl;
    for(unsigned int i = 0; i < land.Height; i++)
    {
        out << '|';
        for(unsigned int j = 0; j < land.Width; j++)
            out << land.Land[i][j];
        out << '|' << std::endl;
    }
    for(unsigned i = 0; i < land.Width + 2; i++)
        out << '-';
    out << std::endl;
}

Map::~Map()
{
    for(unsigned int i = 0; i < Height; i++)
        delete[] Land[i];
    delete Land;
}
