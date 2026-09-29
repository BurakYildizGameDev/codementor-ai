#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Door.generated.h"

UCLASS(Blueprintable)
class MYGAME_API ADoor : public AActor
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Door")
    float OpenSpeed = 2.f // expect-error

    // Kapıyı açar (yorum, eksik ';' tanısını bu satıra kaydırmamalı)
    UFUNCTION(BlueprintCallable)
    void Open();
};
