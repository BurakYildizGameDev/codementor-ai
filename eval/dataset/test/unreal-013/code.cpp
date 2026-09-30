#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "EnemyTracker.generated.h"

UCLASS()
class AEnemyTracker : public AActor
{
    GENERATED_BODY()

public:
    void Register(AActor* Enemy) { Enemies.Add(Enemy); }

    int32 CountValid() const
    {
        int32 Count = 0;
        for (AActor* Enemy : Enemies)
        {
            if (Enemy->IsActorTickEnabled())
            {
                ++Count;
            }
        }
        return Count;
    }

private:
    TArray<AActor*> Enemies;
};
