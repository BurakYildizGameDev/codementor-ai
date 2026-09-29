#include "Mover.h"

void AMover::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    const FVector Delta = Velocity * DeltaTime;
    SetActorLocation(GetActorLocation() + Delta);
    Elapsed += DeltaTime;
}
