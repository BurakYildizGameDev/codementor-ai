#include "Platform.h"

void APlatform::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    FVector Location = GetActorLocation();
    Location += Direction * Speed;
    SetActorLocation(Location);
}
