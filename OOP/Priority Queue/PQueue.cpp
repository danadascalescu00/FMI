#include "PQueue.h"

PQueue::PQueue(int c) : Qsize(0) , capacity(c)
{
    harr = new MinHeap[capacity];
}

PQueue::PQueue(int c, int p, int item)
{
    capacity = c;
    Qsize++;
    harr = new MinHeap[capacity];
    harr[0].priority = p; harr[0].value = item;
}

PQueue::PQueue(const PQueue& PriorityQueue)
{
    Qsize = PriorityQueue.Qsize;
    capacity = PriorityQueue.capacity;
    harr = new MinHeap[capacity];
    for(int i =0 ; i<Qsize; i++)
    {
        harr[i].value = PriorityQueue.harr[i].value;
        harr[i].priority = PriorityQueue.harr[i].priority;
    }
}

PQueue::~PQueue()
{
    Qsize = capacity = 0;
    delete[] harr;
}

PQueue& PQueue::operator= (const PQueue &P)
{
    if(this != &P)
    {
        delete[] harr;
        Qsize = capacity =0;
        capacity = P.capacity;
        Qsize = P.Qsize;
        harr = new MinHeap[P.capacity];
        for(int i =0; i<P.Qsize; i++) {
            harr[i].value = P.harr[i].value;
            harr[i].priority = P.harr[i].priority;
        }
    }
    return *this;
}

ostream& operator<<(ostream& out, PQueue& PQ)
{
    for(int i = 0; i<PQ.Qsize; i++)
        out << PQ.harr[i].value << ' ' <<PQ.harr[i].priority << endl;
    return out;
}

istream& operator>>(istream& in, PQueue& PQ) {

    in >> PQ.capacity;
    in >> PQ.Qsize;
    for (int i = 0; i < PQ.Qsize; i++)
    {
        in >> PQ.harr[i].value;
        in >> PQ.harr[i].priority;
    }
    return in;
}

PQueue PQueue::operator++( )
{
    for(int i = 0; i<Qsize; i++)
    {
        harr[i].IncreasePriority(1);
        int j = i;
        while (j != 0 && harr[left(j)].priority < harr[j].priority) {
            MinHeap temp = harr[j];
            harr[j] = harr[left(j)];
            harr[left(j)] = temp;
            j = left(j);
        }
        while (j != 0 && harr[right(j)].priority < harr[j].priority) {
            MinHeap temp = harr[j];
            harr[j] = harr[right(j)];
            harr[right(j)] = temp;
            j = right(j);
        }
    }
    return *this;
}

PQueue PQueue::operator--()
{
    for( int i=0; i<Qsize; i++)
    {
        harr[i].DecreasePriority(1);
        if(harr[i].priority == 0) deleteItem(i);
        int j = i;
        while (j != 0 && harr[parent(j)].priority > harr[j].priority) {
            MinHeap temp = harr[j];
            harr[j] = harr[parent(j)];
            harr[parent(j)] = temp;
            j = parent(j);
        }
    }
    return *this;
}

bool PQueue::isEmpty() const
{
    return Qsize==0;
}

bool PQueue::isFull() const
{
    return Qsize==capacity;
}

int PQueue::getSize() const
{
    return Qsize;
}

int PQueue::getCapacity() const
{
    return capacity;
}


void PQueue::MinHeapify(int i)
{
    int l = left(i);
    int r = right(i);
    int index_smallest_element = i;
    while(l<Qsize && harr[l].priority < harr[i].priority)
        index_smallest_element = l;
    while(r<Qsize && harr[r].priority < harr[i].priority)
        index_smallest_element = r;
    if(index_smallest_element != i)
    {
        MinHeap temp = harr[index_smallest_element];
        harr[index_smallest_element] = harr[i];
        harr[i] = temp;
        MinHeapify(index_smallest_element);
    }
}

int PQueue::GetTopPriorityElement()
{
    if(Qsize == 1) return harr[0].value;

    MinHeap root = harr[0];
    harr[0] = harr[Qsize-1];
    MinHeapify(0);
    return root.value;
}

void PQueue::deleteItem(int i) //This function deletes item at index i. It first reduces priority to -infinite, then calls the function extractMin.
{
    Decrease(i, INT_MAX);
    extractTopPriority();
}

void PQueue::insertItem(int v, int p)   //Inserting an element of value v and priority p
{
    if(Qsize == capacity)
    {
        std::cout<<"Overflow: Could not insert item\n";
        return;
    }

    Qsize++;
    int i = Qsize - 1;
    harr[i].value = v; harr[i].priority  = p;
    while(i!=0 && harr[parent(i)].priority > harr[i].priority)
    {
        MinHeap aux = harr[i];
        harr[i] = harr[parent(i)];
        harr[parent(i)] = aux;
        i = parent(i);
    }
}

int PQueue::extractTopPriority()
{
    if (Qsize <= 0)
        return INT_MAX;
    if (Qsize == 1)
    {
        Qsize--;
        return harr[0].value;
    }

    // Store the element with top priority, and remove it from heap
    MinHeap root = harr[0];
    harr[0] = harr[Qsize-1];
    Qsize--;
    MinHeapify(0);
    return root.value;
}

void PQueue::Decrease(int i, int p)
{
    harr[i].priority = harr[i].priority - p;
    while(i != 0 && harr[parent(i)].priority > harr[i].priority)
    {
        MinHeap temp = harr[i];
        harr[i] = harr[parent(i)];
        harr[parent(i)] = temp;
        i = parent(i);
    }
}

int PQueue::GetMaximumValue()
{
    int maxi = INT_MIN;
    for(int i=0; i < this->Qsize; i++)
    {
        if (this->harr[i].value > maxi) maxi = this->harr[i].value;
    }
    return maxi;
}

PQueue PQueue::operator + ( PQueue &PQ)
{
    PQueue PQnew;
    PQnew.Qsize = Qsize + PQ.capacity;
    PQnew.capacity = capacity + PQ.capacity;
    PQnew.harr = new MinHeap[PQnew.Qsize + 10];
    for(int i = 0; i<PQnew.Qsize; i++) {
        PQnew.harr[i].value = harr[i].value + PQ.harr[i].value;
        PQnew.harr[i].priority = harr[i].priority + PQ.harr[i].priority;
    }
    PQnew.MinHeapify(0);
    return PQnew;
}
