#include "HealthRegenComponent.h"

UHealthRegenComponent::UHealthRegenComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UHealthRegenComponent::TickComponent(float DeltaTime, ELevelTick TickType,
                                          FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    if (CurrentHealth < MaxHealth)
    {
        CurrentHealth = FMath::Min(CurrentHealth + RegenPerSecond * DeltaTime, MaxHealth);
    }
}
