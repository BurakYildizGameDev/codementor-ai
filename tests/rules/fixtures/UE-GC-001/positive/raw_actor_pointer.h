// EXPECT: 11
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Turret.generated.h"

UCLASS()
class ATurret : public AActor
{
    GENERATED_BODY()
    AActor* Target;
};
