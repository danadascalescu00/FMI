#ifndef GAME_H
#define GAME_H

#include <cmath>
#include <chrono>
#include <thread>

#include "Map.h"
#include "Character.h"
#include "Player.h"
#include "Enemy.h"
#include "Wizard.h"

class Game
{
    protected:
        Map Battlefield;
        Characters characters;
        unsigned int count_rounds;

        void AddCharacters(); //This method puts the characters on the map (initial configuration)
        void EliminateCharacter(const unsigned int& ); //This method will eliminate the character when he is dead
        void Attack(const unsigned int& , const unsigned int& );
    public:
        Game(const unsigned int& , const unsigned int& );
        void operator()(); //Overload operator () for showing the story
        void StartGame();
        ~Game();
};

#endif // GAME_H
