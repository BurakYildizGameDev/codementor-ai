// EXPECT: 9, 14
#include "Squad.h"

void ASquad::CollectNames(const TArray<AActor*>& Actors)
{
    TArray<FString> Names;
    for (AActor* Actor : Actors)
    {
        Names.Add(Actor->GetName());
    }
    TArray<int32> Ids;
    for (int32 i = 0; i < 16; ++i)
    {
        Ids.Emplace(i);
    }
}
