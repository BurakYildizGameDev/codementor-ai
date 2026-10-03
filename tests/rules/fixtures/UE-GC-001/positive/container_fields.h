// EXPECT: 11, 12, 13
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Spawner.generated.h"

UCLASS()
class ASpawner : public AActor
{
    GENERATED_BODY()
    TArray<AActor*> Spawned;
    TMap<FName, UTexture2D*> Icons;
    TArray<TObjectPtr<AEnemy>> Enemies;
    UPROPERTY()
    TArray<AActor*> Tracked;
    TArray<FVector> Points;
    TMap<FName, int32> Counts;
};
