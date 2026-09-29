#include "WaveSpawner.h"
#include "Engine/World.h"
#include "TimerManager.h"

USTRUCT(BlueprintType)
struct FWaveConfig
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere)
    int32 EnemyCount = 10;

    UPROPERTY(EditAnywhere)
    TSubclassOf<AActor> EnemyClass;
};

UCLASS()
class MYGAME_API AWaveSpawner : public AActor
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Waves")
    TArray<FWaveConfig> Waves;

    UFUNCTION()
    void HandleEnemyDestroyed(AActor* DestroyedActor);

protected:
    virtual void BeginPlay() override;

private:
    UPROPERTY()
    TArray<TObjectPtr<AActor>> AliveEnemies;

    UPROPERTY()
    TMap<FName, int32> KillsByType;

    int32 CurrentWave = 0;

    void StartWave();
};

void AWaveSpawner::BeginPlay()
{
    Super::BeginPlay();
    StartWave();
}

void AWaveSpawner::StartWave()
{
    if (!Waves.IsValidIndex(CurrentWave))
    {
        return;
    }
    const FWaveConfig& Config = Waves[CurrentWave];
    AliveEnemies.Reset();
    AliveEnemies.Reserve(Config.EnemyCount);
    for (int32 i = 0; i < Config.EnemyCount; ++i)
    {
        AActor* Enemy = GetWorld()->SpawnActor<AActor>(Config.EnemyClass, GetActorTransform());
        if (IsValid(Enemy))
        {
            Enemy->OnDestroyed.AddDynamic(this, &AWaveSpawner::HandleEnemyDestroyed);
            AliveEnemies.Add(Enemy);
        }
    }
}

void AWaveSpawner::HandleEnemyDestroyed(AActor* DestroyedActor)
{
    AliveEnemies.RemoveSwap(DestroyedActor);
    KillsByType.FindOrAdd(DestroyedActor->GetClass()->GetFName())++;
    if (AliveEnemies.Num() == 0)
    {
        ++CurrentWave;
        StartWave();
    }
}
