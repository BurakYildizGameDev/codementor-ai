#include "RegenComponent.h"
#include "GameFramework/Character.h"

void URegenComponent::BeginPlay()
{
    Super::BeginPlay();
    ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
    OwnerCharacter->GetCharacterMovement()->MaxWalkSpeed *= SpeedMultiplier;
}
