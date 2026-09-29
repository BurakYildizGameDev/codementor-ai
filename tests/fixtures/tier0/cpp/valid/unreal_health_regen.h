#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HealthRegenComponent.generated.h"

UENUM(BlueprintType)
enum class ERegenState : uint8
{
    Idle UMETA(DisplayName = "Bekliyor"),
    Regenerating UMETA(DisplayName = "Yenileniyor")
};

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class MYGAME_API UHealthRegenComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHealthRegenComponent();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Regen",
              meta = (ClampMin = "0.0", UIMin = "0.0"))
    float RegenPerSecond = 5.f;

    UPROPERTY(EditAnywhere, Category = "Regen")
    float DelayAfterDamage = 3.f;

    UFUNCTION(BlueprintCallable, Category = "Regen")
    void NotifyDamaged();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType,
                               FActorComponentTickFunction* ThisTickFunction) override;

private:
    UPROPERTY(VisibleAnywhere)
    ERegenState State = ERegenState::Idle;

    FTimerHandle DelayHandle;
};
