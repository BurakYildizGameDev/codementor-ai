#include "Spawner.h"
#include "Kismet/GameplayStatics.h"

void ASpawner::BeginPlay()
{
    Super::BeginPlay();
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AEnemy::StaticClass(), Enemies);
    for (AActor* Enemy : Enemies)
    {
        Enemy->SetActorHiddenInGame(false);
    }
}
