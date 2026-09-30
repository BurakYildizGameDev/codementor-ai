#include "GameFramework/Actor.h"

void AFloatingActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    FVector Location = GetActorLocation()
    Location.Z += FMath::Sin(GetGameTimeSinceCreation()) * 20.0f * DeltaTime;
    SetActorLocation(Location);
}
