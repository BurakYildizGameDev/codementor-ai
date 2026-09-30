#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HealComponent.generated.h"

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class UHealComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere)
    float HealPerSecond = 5.0f;

    void SetHealTarget(AActor* NewTarget) { HealTarget = NewTarget; }

private:
    AActor* HealTarget = nullptr;
};
