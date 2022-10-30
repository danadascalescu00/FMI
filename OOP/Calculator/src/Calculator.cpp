#include "Calculator.h"

#ifdef __WIN32
#define CLEAR "CLS"
#elif __unix__
#define CLEAR "clear"
#endif

using namespace std;

Calculator::Calculator() : memory(0)
{
    read = false;
}

void Calculator::DisplayLegend()
{
    std::cout<<std::endl<<'\t'<< "ADD -> + " <<std::endl;;
    std::cout<<'\t'<< "SUB -> - " <<std::endl;
    std::cout<<'\t'<< "Multiply -> * " <<std::endl;
    std::cout<<'\t'<< "Divide -> / " <<std::endl;
    std::cout<<'\t'<< "POW -> ^ " <<std::endl;
    std::cout<<'\t'<< "SQRT -> sqrt " <<std::endl;
    std::cout<<'\t'<< "MemSet -> MS " <<std::endl;
    std::cout<<'\t'<< "MemClear -> MC " <<std::endl;
    std::cout<<'\t'<< "MemPlus -> M+ " <<std::endl;
    std::cout<<'\t'<< "MemMinus -> M- " <<std::endl;
    std::cout<<'\t'<< "Clear -> C " <<std::endl;
    std::cout<<'\t'<< "Quit -> q " <<std::endl<<std::endl;
}

Calculator::~Calculator()
{
    cout<<endl<<"Existing now...."<<endl;
    this_thread::sleep_for(chrono::seconds(3));
}

void Calculator::operator()()
{
    auto start_time = std::chrono::high_resolution_clock::now();
    do{
            read = false;
            if(!read)
            {
                cout<<"Enter the first operand: ";
                cin>>first_operand;
                read = true;
            }
            try{
                    std::cout<<"Enter operation: ";
                    std::cin>>user_input;
            }catch(std::exception e){
                system(CLEAR);
                cout << e.what() << endl;
                this_thread::sleep_for(chrono::seconds(2));
                continue;
            }
            if(user_input.GetArity() == 1)
            {
                switch(user_input.GetSymbol())
                {
                    case 't' : {
                        cout<< first_operand;
                        std::cout<< user_input;
                        system(CLEAR);
                        cout<< first_operand.SquareRoot();
                        cout<< endl << '\t';
                        DisplayLegend();
                        break;
                    }
                    case 'S' :{
                        system(CLEAR);
                        memory = first_operand;
                        DisplayLegend();
                        break;
                    }
                    case 'r' :{
                        system(CLEAR);
                        memory = 0;
                        DisplayLegend();
                        break;
                    }
                    case '+' :{
                        system(CLEAR);
                        cout<< first_operand + memory;
                        DisplayLegend();
                        break;
                    }
                    case '-' :{
                        system(CLEAR);
                        std::cout<< first_operand - memory << std::endl;
                        DisplayLegend();
                        break;
                    }
                    case 'C' :{
                        first_operand = 0;
                        read = false;
                    }
                    default:
                        break;
                }
                continue;
            }
            std::cout<< first_operand << ' ';
            std::cout<< user_input <<' ';
            std::cin>>second_operand;
            if(user_input.GetArity() == 2)
            {
                switch(user_input.GetSymbol())
                {
                    case '+' :{
                        system(CLEAR);
                        std::cout<< " = " << first_operand + second_operand << std::endl;
                        DisplayLegend();
                        break;
                    }
                    case '-' :{
                        system(CLEAR);
                        std::cout<< " = " << first_operand - second_operand << std::endl;
                        DisplayLegend();
                        break;
                    }
                    case '*' :{
                        system(CLEAR);
                        std::cout<< " = " << first_operand * second_operand << std::endl;
                        DisplayLegend();
                        break;
                    }
                    case '/' :{
                        system(CLEAR);
                        try{
                            std::cout<< " = " << first_operand / second_operand << std::endl;
                            break;
                        }catch(invalid_argument ba)
                        {
                            std::cout<< "Invalid argument for the second operand." << std::endl;
                        }
                        DisplayLegend();
                        break;
                    }
                    case '^' :{
                        system(CLEAR);
                        float temp = first_operand ^ second_operand;
                        cout<< " = " << temp << endl;
                        DisplayLegend();
                        break;
                    }
                    default:
                        break;
                }
                continue;
            }
            system(CLEAR);
        DisplayLegend();
    }while(this->user_input.GetSymbol() != 'q');
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double , std::milli> elapsed = end_time - start_time;
    std::cout<<"Session ended after "<< elapsed.count() << "ms."<<std::endl;
}
