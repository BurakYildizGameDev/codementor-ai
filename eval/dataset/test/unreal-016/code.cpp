#include "DamageFeed.h"
#include "DamageEvent.h"

void ADamageFeed::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    UDamageEvent* Event = NewObject<UDamageEvent>(this);
    Event->Amount = PendingDamage;
    PendingDamage = 0.0f;
    Broadcast(Event);
}
