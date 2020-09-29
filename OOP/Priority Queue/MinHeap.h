#ifndef MINHEAP_H
#define MINHEAP_H

#include <iostream>
#include <climits>
#include <limits>

using namespace std;

class PQueue;

class MinHeap
{
        int value, priority;
    public:
        MinHeap(); //Constructor without parameters
        MinHeap(int , int); //Constructor with parameters
        //~MinHeap(); //There is no need for a destructor
        int GetValue() const;
        int GetPriority() const;
        void SetValue(int );
        void SetPriority(int );
        void IncreaseValue(int );
        void IncreasePriority(int );
        void DecreaseValue(int );
        void DecreasePriority(int );
        friend class PQueue;
        friend ostream& operator<<(ostream& , PQueue&);
        friend istream& operator>>(istream& , PQueue&);
};

#endif // MINHEAP_H
