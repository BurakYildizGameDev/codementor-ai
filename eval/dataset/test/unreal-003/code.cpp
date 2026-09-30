#include "GameFramework/Actor.h"

int32 CountAlive(const TArray<AActor*& Actors)
{
    int32 Alive = 0;
    for (AActor* Actor : Actors)
    {
        if (IsValid(Actor))
        {
            ++Alive;
        }
    }
    return Alive;
}
