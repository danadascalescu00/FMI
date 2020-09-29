#include "MinHeap.h"

MinHeap::MinHeap()
{
    value = 0;
    priority = INT_MIN;
}

MinHeap::MinHeap(int v, int p) : value(v) , priority(p)
{
}

int MinHeap::GetValue() const
{
    return this->value;
}

int MinHeap::GetPriority() const
{
    return priority;
}

void MinHeap::SetValue(int x)
{
    value = x;
}

void MinHeap::SetPriority(int y)
{
    priority = y;
}

void MinHeap::IncreaseValue(int val)
{
    value += val;
}

void MinHeap::DecreaseValue(int v)
{
    value = value - v;
}

void MinHeap::IncreasePriority(int pri)
{
    priority += pri;
}

void MinHeap::DecreasePriority(int p)
{
    priority = priority - p;
}
