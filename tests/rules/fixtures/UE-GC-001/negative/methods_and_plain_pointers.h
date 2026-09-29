#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Turret.generated.h"

UCLASS()
class ATurret : public AActor
{
    GENERATED_BODY()
public:
    AActor* GetTarget() const;
private:
    FVector* CachedLocation;
    int32* Scores;
    TWeakObjectPtr<AActor> LastHit;
};
