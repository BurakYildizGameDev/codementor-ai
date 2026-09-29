// EXPECT: 8
#include "Health.h"

void UHealth::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    float Total = 0.f;
    for (const FEffect& Effect : Effects)
    {
        Total += Effect.Amount;
    }
    Health -= Total * DeltaTime;
}
