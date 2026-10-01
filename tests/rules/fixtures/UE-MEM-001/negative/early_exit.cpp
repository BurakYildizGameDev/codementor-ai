#include "Squad.h"

void ASquad::Alive(const TArray<AActor*>& Actors)
{
    TArray<AActor*> Alive;
    for (int32 i = 0; i < Actors.Num(); ++i)
    {
        if (Actors[i] == nullptr) continue;
        Alive.Add(Actors[i]);
    }
    TArray<int32> FirstTen;
    for (int32 i = 0; i < Actors.Num(); ++i)
    {
        if (i >= 10) break;
        FirstTen.Add(i);
    }
}
