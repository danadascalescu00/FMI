#include <cstdlib>
#include <ctime>
#include "Game.h"

unsigned int choice, width, height;

void Legend()
{
    std::cout<<std::endl;
    std::cout<<'\t'<<'\t'<<"The Shootout"<<std::endl;
    std::cout<<"Player: P"<<std::endl<<"Enemy: E"<<std::endl<<"Wizard: W";
    std::cout<<std::endl<<std::endl;
    std::cout<<'\t'<<"About the game: "<<std::endl;
    std::cout<<"This game is a zero-player game, meaning that its evolution is determinated by its initial state,"<<std::endl;
    std::cout<<"requiring no further input. One interacts with The Shootout by creating an initial configuration and"<<std::endl;
    std::cout<<"observing how it evolves."<<std::endl<<std::endl<<std::endl;
}

int main()
{
    std::cout<<'\t'<<'\t'<<'\t'<<"Welcome to the Shootout Battle!"<<std::endl;

    do{
        std::cout<<"Press 1 for showing the legend"<<std::endl<<"Press 2 to start the game"<<std::endl<<"Press 3 to exit the menu"<<std::endl<<std::endl;
        std::cout<<std::endl;
        std::cout<<"Please enter your choice: ";
        std::cin>>choice;
        switch(choice)
        {
            case 1 :{
                Legend();
                break;
            }
            case 2 :{
                std::cout<<std::endl;
                std::cout<<"Choose the map"<<std::endl;
                std::cout<<"Dimension of the map (min. 25x25): ";
                std::cout<<"Insert height: "<<std::endl;
                do{ std::cin>>height;
                    if(height < 25) std::cout<<"Insert another value!"<<std::endl;
                  }while(height < 25);
                std::cout<<"Insert width: "<<std::endl;
                do{ std::cin>>width;
                    if(width < 25) std::cout<<"Insert another value!"<<std::endl;
                  }while(width < 25);

                srand((unsigned int)time(0));

                Game battle(height, width);
                battle();
                battle.StartGame();
                break;
            }
            case 3 :
                break;
            default:
                std::cout<<std::endl<<"Wrong choice!"<<std::endl;
                break;
        }
    }while(choice!=3);

    return 0;
}
