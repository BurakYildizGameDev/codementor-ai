#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "WaveSpawner.generated.h"

UCLASS()
class AWaveSpawner : public AActor
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override
    {
        Super::BeginPlay();
        GetWorldTimerManager().SetTimer(WaveTimer, this, &AWaveSpawner::SpawnWave, WaveInterval, true);
    }

    void SpawnWave()
    {
        for (int32 i = 0; i < EnemiesPerWave; ++i)
        {
            if (AActor* Enemy = GetWorld()->SpawnActor<AActor>(EnemyClass, GetActorTransform()))
            {
                Alive.Add(Enemy);
            }
        }
    }

    UPROPERTY(EditAnywhere)
    TSubclassOf<AActor> EnemyClass;

    UPROPERTY(EditAnywhere)
    int32 EnemiesPerWave = 5;

    UPROPERTY(EditAnywhere)
    float WaveInterval = 10.0f;

    UPROPERTY()
    TArray<TObjectPtr<AActor>> Alive;

    FTimerHandle WaveTimer;
};
