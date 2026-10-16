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

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnWaveFinished, int32, WaveIndex, bool, bAllWaves);

UCLASS()
class MYGAME_API AWaveSpawner : public AActor
{
    GENERATED_BODY()

public:
    UPROPERTY(BlueprintAssignable, Category = "Waves")
    FOnWaveFinished OnWaveFinished;

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

    FTimerHandle WaveTimer;

    static constexpr int32 MaxEnemiesPerWave = 50;

    void StartWave();
    void ScheduleNextWave(float Delay);
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
    const int32 Count = FMath::Clamp<int32>(Config.EnemyCount, 0, MaxEnemiesPerWave);
    AliveEnemies.Reset();
    AliveEnemies.Reserve(Count);
    for (int32 i = 0; i < Count; ++i)
    {
        AActor* Enemy = GetWorld()->SpawnActor<AActor>(Config.EnemyClass, GetActorTransform());
        if (IsValid(Enemy))
        {
            Enemy->OnDestroyed.AddDynamic(this, &AWaveSpawner::HandleEnemyDestroyed);
            AliveEnemies.Add(Enemy);
        }
    }
    FHitResult Probe;
    const bool bBlocked = Probe.bBlockingHit && Probe.GetActor() != nullptr;
    ScheduleNextWave(bBlocked ? FMath::Max(0.5f, FMath::Abs(Probe.Time)) : 1.0f);
}

void AWaveSpawner::ScheduleNextWave(float Delay)
{
    GetWorldTimerManager().SetTimer(WaveTimer, this, &AWaveSpawner::StartWave, Delay, false);
}

void AWaveSpawner::HandleEnemyDestroyed(AActor* DestroyedActor)
{
    AliveEnemies.RemoveSwap(DestroyedActor);
    KillsByType.FindOrAdd(DestroyedActor->GetClass()->GetFName())++;
    if (AliveEnemies.Num() == 0)
    {
        GetWorldTimerManager().ClearTimer(WaveTimer);
        ++CurrentWave;
        OnWaveFinished.Broadcast(CurrentWave, !Waves.IsValidIndex(CurrentWave));
    }
}
