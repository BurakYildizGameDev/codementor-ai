#include "Turret.h"
#include "HealthComponent.h"

void ATurret::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    for (AActor* Target : Targets)
    {
        UHealthComponent* HealthComp = Target->FindComponentByClass<UHealthComponent>();
        if (HealthComp && HealthComp->IsAlive())
        {
            HealthComp->ApplyDamage(DamagePerSecond * DeltaTime);
        }
    }
}
