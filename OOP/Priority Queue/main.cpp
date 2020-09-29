#include "MinHeap.h"
#include "PQueue.h"

#include <cassert>

void PrintVector(int *v, unsigned int n)
{
    for(unsigned int i = 0; i < n; i++)
        std::cout<<v[i]<<' ';
    delete[] v;
}

int main()
{
    int choice;
    std::cout<<"1.Insert an element"<<endl;
    std::cout<<"2.Remove element"<<endl;
    std::cout<<"3.Display the number of elements from queue"<<endl;
    std::cout<<"4.Merge two queues"<<endl;
    std::cout<<"5.Increase with 1 the priorities of the elements in the queue"<<endl;
    std::cout<<"6.Decrease with 1 the priorities of the elements in the queue"<<endl;
    std::cout<<"7.Get top priority element"<<endl;
    std::cout<<"8.Get the maximum value"<<endl;
    std::cout<<"9.Display"<<endl;
    std::cout<<"10.Quit"<<endl;
    PQueue PQ;
    do
    {
        cout<<"Enter your choice: "<<endl;
        cin>>choice;
        switch(choice)
        {
            case 1: {
                int Value, Priority;
                std::cout<<"Enter the value for the new element in the queue: ";
                std::cin>>Value;
                std::cout<<"Enter the priority for the new element in the queue: ";
                std::cin>>Priority;
                PQ.insertItem(Value, Priority);
                break;
            }
            case 2: {
                std::cout<<"The size of the queue is: ";
                cout<< PQ.getSize();
                std::cout<< std::endl;
                std::cout<<"Enter the index of the element to be deleted: ";
                int index;
                do{
                    std::cin>>index;
                    if(index >= PQ.getSize()) std::cout<< "Enter another index: ";
                }while(index >= PQ.getSize());
                PQ.deleteItem(index);
                break;
            }
            case 3:
                std::cout<<PQ.getSize()<<endl;
                break;
            case 4: {
                PQueue PQ1(10, 10, 3);
                PQ1.insertItem(16, 14);
                PQ1.insertItem(20, 1);
                PQueue PQ2(10, 5, 12);
                PQ2.insertItem(20, 2);
                PQueue PQ3;
                PQ3 = PQ1 + PQ2;
                cout << PQ3;
                break;
            }
            case 5: {
                PQueue PQ2(20, 5, 10);
                std::cout<<"Old queue: ";
                cout<< PQ2;
                ++PQ2;
                std::cout<<"New queue: ";
                cout<<PQ2;
                break;
            }
            case 6: {
                --PQ;
                cout<<PQ;
                break;
            }
            case 7:
                std::cout<<PQ.GetTopPriorityElement()<<endl;
                break;
            case 8:
                std::cout<<PQ.GetMaximumValue()<<endl;
                break;
            case 9:
                assert(PQ.isEmpty() == false);
                cout << PQ;
            case 10:
                break;
            default:
                cout<<"Wrong choice"<<endl;
                break;
        }
    }while(choice != 10);
    
    return 0;
}
