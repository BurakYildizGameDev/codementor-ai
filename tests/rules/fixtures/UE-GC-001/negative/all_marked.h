#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Turret.generated.h"

UCLASS()
class ATurret : public AActor
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, Category = "Turret")
    AActor* Target;

    UPROPERTY(VisibleAnywhere)
    TObjectPtr<UStaticMeshComponent> Barrel;
};
