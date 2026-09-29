// EXPECT: 13
#pragma once
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Inventory.generated.h"

UCLASS()
class UInventory : public UActorComponent
{
    GENERATED_BODY()
    UPROPERTY()
    UStaticMesh* Mesh;
    TObjectPtr<UMaterialInterface> Material;
};
