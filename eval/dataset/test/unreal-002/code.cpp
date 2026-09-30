#include "Components/ActorComponent.h"

void UAmmoComponent::Fire()
{
    if (CurrentAmmo <= 0 {
        UE_LOG(LogTemp, Warning, TEXT("Mermi yok"));
        return;
    }
    --CurrentAmmo;
}
