#include "Game.h"

#ifdef __WIN32
#define Clear "CLS"
#elif __unix__
#define Clear "clear"
#endif // __WIN32

void Game::AddCharacters()
{
    Positions pos;
    Character *c;

    unsigned int width = Battlefield.GetWidth();
    unsigned int height = Battlefield.GetHeight();

    for(int i = 0; i <= 9; i++)
    {
        Position pos;
        pos.first = rand() % height;
        pos.second = rand() % width;

        switch(i)
        {
            case 0 :
                c = new Wizard(pos);
                break;
            case 1 :
                c = new Enemy(pos);
                break;
            case 2 :
                c = new Enemy(pos);
                break;
            case 3 :
                c = new Enemy(pos);
                break;
            case 4 :
                c = new Enemy(pos);
                break;
            case 5 :
                c = new Enemy(pos);
                break;
            case 6 :
                c = new Enemy(pos);
                break;
            case 7 :
                c = new Enemy(pos);
                break;
            case 8 :
                c = new Enemy(pos);
                break;
            case 9 :
                c = new Player(pos);
                break;
        }
        characters.push_back(c); //We add our character in vector
        Battlefield.AddCell(c->GetPosition(), c->GetCharacter());
    }
}

void Game::EliminateCharacter(const unsigned int& val)
{
    std::cout<<"Character "<<characters[val]->GetCharacter()<<" died."<<std::endl;
    Position pos = characters[val]->GetPosition();
    Battlefield.AddCell(pos, ' ' );
    characters.erase(characters.begin() + val);
}

void Game::Attack(const unsigned int& i, const unsigned int& j)   //Character with index i attacks character with index j
{
    std::cout<< "Character " << characters[i]->GetCharacter() <<" from the position ";
    cout<<characters[i]->GetPosition();
    std::cout<< " attacks character " << characters[j]->GetCharacter() <<" from the position ";
    cout<<characters[j]->GetPosition();
    std::cout<<std::endl;

    double weapon_damage = characters[i]->weapon->GetDamage();
    double opponent_health = characters[j]->GetHealth();
    int opponent_life = characters[j]->GetLife();
    unsigned int index =characters.size() - 1;
    if(j == index)   //If the character is a player
    {
        double opponent_bonushealth = characters[j]->armor->GetBonusHealth();
        double opponent_bonusdamageweapon = characters[j]->armor->GetBonusDamageWeapon();
        double opponent_damage_weapon = characters[j]->weapon->GetDamage();
        opponent_damage_weapon = opponent_damage_weapon + opponent_bonusdamageweapon; //The armor gives the player a bonus damage weapon each time he uses it
        characters[j]->weapon->SetDamage(opponent_damage_weapon); //Increase the damage of the weapon after the armor was used
        std::cout<<"Opponent "<<characters[j]->GetCharacter() <<" countered the attack with his armor."<<std::endl;
        opponent_health = opponent_health + opponent_bonushealth;
        opponent_health = opponent_health - weapon_damage;
        characters[j]->SetHealth(opponent_health);
        if(characters[j]->GetHealth() <= 0)
        {
            opponent_life--;
            characters[j]->SetLife(opponent_life);
            double opponent_new_health = 100.0 + characters[j]->GetHealth();
            characters[j]->SetHealth(opponent_new_health);
        }
        }else{
            opponent_health = opponent_health - weapon_damage;
            characters[j]->SetHealth(opponent_health);
            if(characters[j]->GetHealth() <= 0)
            {
                opponent_life--;
                characters[j]->SetLife(opponent_life);
                double opponent_new_health = 100.0 + characters[j]->GetHealth();
                characters[j]->SetHealth(opponent_new_health);
            }
         }
}

void Game::operator()()
{
    std::cout<<'\t'<<"Can you conquer your enemies in Shootout Battle?"<<std::endl;
    std::cout<<"You control an elite combat soldier and must shoot your enemies in order to conquer the land. "<<std::endl;
    std::cout<<"The game takes place in rounds. Each character has one move per round and must decide either he moves or attacks"<<std::endl;
    std::cout<<"(Pay attention that you can't move if an enemy is in your sight). Some enemies can be killed in two shots, "<<std::endl;
    std::cout<<"others take several shots to dispatch. Be carefull that some enemies(wizards) can come back to life."<<std::endl;
    std::cout<<"Good luck!"<<std::endl<<std::endl;
}

void Game::StartGame()
{
    char user_choice; //The user will have to decide after each round if he wants to continue the game
    bool user_is_playing = true;
    bool player_has_died = false;
    bool there_is_one_character_left = false;
    unsigned int count_characters = characters.size();
    do{
        system(Clear);
        count_rounds++;
        std::cout<<"Round "<<count_rounds<<'\n' ;
        for(unsigned int i = 0; i < characters.size(); i++) //Each character can do one move (attack or move) per round
        {
            Position pos = characters[i]->GetPosition();   //Current position of the character on the map
            unsigned int temp = characters[i]->GetArea();
            Position new_pos = characters[i]->NextMove(Battlefield, pos, temp); //Calculate the next position of the character depending on its area of vision
            if(characters[i]->canMove(Battlefield, pos, temp) == true)    //The character is allowed to move only if in it's area(third parameter)
            {                                                            //there isn't another character
                if(pos != new_pos)
                {
                    std::cout<<"Character "<<characters[i]->GetCharacter()<<" from ";
                    cout<<pos;
                    std::cout<<" changed his position to ";
                    cout<<new_pos;
                    std::cout<<'.'<<'\n';

                    try{
                            Battlefield.AddCell(pos, ' ');
                            Battlefield.AddCell(new_pos, characters[i]->GetCharacter());
                            characters[i]->Move(new_pos);

                        }catch(std::exception e){}
                }
            }
            if(characters[i]->canMove(Battlefield, pos, temp) == false)  //If the character can't move it means that he must attack the opponent.But if his
            {                                              // weapon's range is smaller than the distance to the opponent, the opponent can try to attack back
                Position pos_attack = characters[i]->FindOut(Battlefield, pos, temp);  //Find out the position of the opponent on the map
                for(unsigned int j = 0; j < characters.size() && i!=j; j++)
                {
                    Position posi = characters[j]->GetPosition();
                    if(posi.first == pos_attack.first && posi.second == pos_attack.second)
                    {
                            unsigned int weapon_range = characters[i]->weapon->GetRange();
                            double h_distance, w_distance;
                            h_distance = (double)pos.first - (double)pos_attack.first;
                            w_distance = (double)pos.second - (double)pos_attack.second;
                            if(std::abs(h_distance) < (double)weapon_range && std::abs(w_distance) < (double)weapon_range)
                            {
                                if(i == 0) //If the character is a wizard he can attack twice;
                                {
                                    Attack(i, j);
                                }
                                Attack(i, j);
                                Attack(j, i);
                                if(characters[j]->isDead())
                                {
                                    unsigned int index = characters.size() - 1;
                                    player_has_died = false;
                                    if(j == index) player_has_died = true;
                                    if(j == 0)  //If the character is a wizard he might rise from dead
                                    {
                                        if(characters[j]->weapon->canRiseFromDead())
                                        {
                                            int wizard_life = 1;
                                            characters[j]->SetLife(wizard_life);
                                            characters[j]->weapon->RiseFromDead();
                                            std::cout<<"The wizard rised from dead."<<std::endl;
                                        }
                                        else{
                                                EliminateCharacter(j);
                                                j--;
                                            }
                                    }else{
                                            EliminateCharacter(j);
                                            j--;
                                         }

                                 }
                                if(characters[i]->isDead())
                                {
                                    unsigned int index = characters.size() - 1;
                                    player_has_died = false;
                                    if(i == index) player_has_died = true;
                                    if(i == 0)  //If the character is a wizard he might rise from dead
                                    {
                                        if(characters[i]->weapon->canRiseFromDead())
                                        {
                                            int wizard_life = 1;
                                            characters[i]->SetLife(wizard_life);
                                            characters[i]->weapon->RiseFromDead();
                                            std::cout<<"The wizard rised from dead."<<std::endl;
                                        }
                                        else{
                                                EliminateCharacter(i);
                                                i--;
                                            }
                                    }else{
                                            EliminateCharacter(i);
                                            i--;
                                         }

                                 }
                            }else{
                                    unsigned int opponent_weapon_range = characters[j]->weapon->GetRange();
                                    if(std::abs(h_distance) < (double)opponent_weapon_range && std::abs(w_distance) < (double)opponent_weapon_range)
                                    {
                                        Attack(j, i);
                                        if(characters[i]->isDead())
                                        {
                                            if(i == 0) player_has_died = true;
                                            EliminateCharacter(i);
                                            i++; j=0;
                                        }
                                    }
                                 }
                     }
                }

            }
        }
        for(unsigned int i = 0; i < characters.size(); i++)
        {
            std::cout<< "Character ";
            std::cout<< characters[i]->GetCharacter();
            std::cout<< " has ";
            std::cout<< characters[i]->GetLife();
            std::cout<<" lives and ";
            std::cout<< characters[i]->GetHealth();
            std::cout<< " health."<<'\n';
        }
        std::cout << Battlefield << std::endl;    //After each round the battlefield will be shown with its changes
        std::cout  << "Would you like to continue playing this game?" << std::endl;
        std::cout << "Press Y for yes and N for no : " <<std::endl;
        std::cin >> user_choice;
        count_characters = characters.size();
        if(count_characters == 1) there_is_one_character_left = true;
        if(user_choice == 'N') user_is_playing = false;    //The simulation will be stop after the user will decide so
    }while(user_is_playing && !player_has_died && !there_is_one_character_left);

    if(user_is_playing == false) std::cout<<"You didn't finish the game!"<<std::endl<<std::endl;
    if(player_has_died) std::cout<<"Game over! You losed!"<<std::endl<<std::endl;
        else std::cout<<"You win!"<<std::endl<<std::endl;
}

Game::Game(const unsigned int& width, const unsigned int& height) : count_rounds(0) , Battlefield(width, height)
{
    AddCharacters();
    std::cout<< "The game has started!"<<std::endl;
    cout << Battlefield;
}

Game::~Game()
{
    count_rounds = 0;
    std::cout<<"The game is over!"<<std::endl;
    std::cout<<"Exiting now..."<<std::endl;
    this_thread::sleep_for(chrono::seconds(3));
}
