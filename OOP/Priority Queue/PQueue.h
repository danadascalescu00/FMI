#ifndef PQUEUE_H
#define PQUEUE_H

#include "MinHeap.h"

#include <stdexcept>

class MinHeap;

class PQueue
{
        MinHeap *harr; //pointer to array of elements in heap
        int Qsize, capacity;
    public:
        PQueue(int = 20);
        PQueue(int , int, int); //Constructor with parameters
        PQueue(const PQueue& ); //Copy-constructo
        ~PQueue(); //Destructor
        PQueue& operator=(const PQueue& );   // Assignment operator
        int parent(int i){ return (i-1)/2; } //returns the parent node
        int left(int i){ return (2*i+1); } //returns the left child node
        int right(int i) { return (2*i+2); } //returns the right child node
        friend ostream& operator<<(ostream& , PQueue&);
        friend istream& operator>>(istream& , PQueue&);
        bool isEmpty() const;
        bool isFull() const;
        int getSize() const;
        int getCapacity() const;
        void MinHeapify(int );
        void deleteItem(int);
        void insertItem(int, int); //Inserting a new item in Queue
        int extractTopPriority();
        void Decrease(int, int);
        int GetTopPriorityElement();
        int GetMaximumValue();
        PQueue operator + ( PQueue&);
        PQueue operator ++( );
        PQueue operator --( );
        friend class MinHeap;
};

#endif // PQUEUE_H
