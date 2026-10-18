// EXPECT: 9, 10
#pragma once
#include "CoreMinimal.h"

UCLASS()
class AHolder : public AActor
{
    GENERATED_BODY()
    TMap<FName, TArray<UObject*>> Nested;
    TArray<TSet<AActor*>> Deep;
    UPROPERTY()
    TMap<FName, TArray<UObject*>> Tracked;
    TMap<FName, TArray<TArray<UObject*>>> TooDeep;
};
