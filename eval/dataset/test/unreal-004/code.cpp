#include "GameFramework/Character.h"

void AHeroCharacter::BeginPlay()
{
    Super::BeginPlay();
    if (HasAuthority())
    {
        Health = MaxHealth;
    }

void AHeroCharacter::Heal(float Amount)
{
    Health = FMath::Min(Health + Amount, MaxHealth);
}
