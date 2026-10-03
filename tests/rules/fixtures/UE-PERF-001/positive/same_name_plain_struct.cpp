// EXPECT: 8
#include "Spawner.h"
#include "Kismet/GameplayStatics.h"

void ASpawner::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), AEnemy::StaticClass(), Enemies);
}

// Faz 32: aynı adlı ama tabansız yapının Tick'i motor tarafından çağrılmaz, sıcak değil
struct FPlanner
{
    void Tick(float DeltaTime)
    {
        UGameplayStatics::GetAllActorsOfClass(nullptr, AEnemy::StaticClass(), Cache);
    }
};
