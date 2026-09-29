#include "TurretComponent.h"
#include "GameFramework/Actor.h"

UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class MYGAME_API UTurretComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, Category = "Turret")
    float Range = 1500.f;

    UPROPERTY()
    TArray<TObjectPtr<AActor>> Targets;

    AActor* CurrentTarget;

    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType,
                               FActorComponentTickFunction* ThisTickFunction) override;

private:
    UFUNCTION()
    void HandleOwnerDestroyed(AActor* DestroyedActor);

    int32 CountVisible(const TArray<AActor*>& Candidates) const;
};

void UTurretComponent::BeginPlay()
{
    Super::BeginPlay();
    GetOwner()->OnDestroyed.AddDynamic(this, &UTurretComponent::HandleOwnerDestroyed);
}

void UTurretComponent::TickComponent(float DeltaTime, ELevelTick TickType,
                                     FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    for (AActor* Target : Targets)
    {
        for (int32 i = 0; i < Targets.Num(); ++i)
        {
            if (Targets[i] != Target && Targets.Contains(Target))
            {
                CurrentTarget = Target;
            }
        }
    }
    FString Label = FString(TEXT("Targets: ")) + FString::FromInt(Targets.Num());
}

int32 UTurretComponent::CountVisible(const TArray<AActor*>& Candidates) const
{
    int32 Count = 0;
    for (int32 Step = 1; Step < Candidates.Num(); Step *= 2)
    {
        ++Count;
    }
    return Count;
}

void UTurretComponent::HandleOwnerDestroyed(AActor* DestroyedActor)
{
    Targets.Empty();
}
