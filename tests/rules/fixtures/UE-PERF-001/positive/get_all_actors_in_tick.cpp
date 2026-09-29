// EXPECT: 8
#include "Spawner.h"
#include "Kismet/GameplayStatics.h"

void ASpawner::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AEnemy::StaticClass(), Enemies);
}
