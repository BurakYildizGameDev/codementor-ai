#pragma once
#include "CoreMinimal.h"

UCLASS()
class AHolder : public AActor
{
    GENERATED_BODY()
    TWeakObjectPtr<AActor> Weak;
    TStrongObjectPtr<UObject> Strong;
    TSoftObjectPtr<UTexture2D> Soft;
    TArray<FVector> Points;
    TMap<FName, int32> Counts;
};
