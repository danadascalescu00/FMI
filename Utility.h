#ifndef UTILITY_H
#define UTILITY_H

#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Character;
class Weapon;

typedef pair<unsigned int ,unsigned int> Position;
typedef vector<Position > Positions;
typedef vector<Character* > Characters;
typedef vector<Weapon* > Weapons;

ostream& operator<<(ostream&, const Position& );

#endif // UTILITY_H
